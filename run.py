"""One command for the whole validated PPNR pipeline.

    python3 run.py                                        # synthetic demo chain, zero setup
    python3 run.py --config config/runs/company.toml      # company run (all stages)
    python3 run.py --check --config <cfg>                 # compose + validate config, run nothing
    python3 run.py --only loans securities --config <cfg> # subset (canonical order kept)
    python3 run.py --only nii --config <cfg> --out out/<previous-run>   # reuse earlier CSVs

Stages, in order (each is the existing examples/ runner, executed in-process so
the printed reports stay byte-identical with the manual commands):

    loans       examples/run_loans.py       --report --paths-out
    securities  examples/run_securities.py  --report --paths-out --paths-basis
    expense     examples/run_from_config.py --report
    nii         examples/run_nii.py         --report --component-paths <loans+securities CSVs>

loans/securities/expense are mutually independent and all run even if one fails;
nii needs both component CSVs and is skipped (nonzero exit) when either is
missing. With no --config every stage runs its own self-contained synthetic demo
(no cross-feeding — outputs match the standalone demos exactly).

All artifacts land in --out (default out/<timestamp>/, gitignored): the four
reports, the two component CSVs, effective_config.txt (key = value  # source),
and run_summary.txt. They carry firm amounts on company runs — keep them local.

SCENARIO NOTE: --scenario is a [mev.scenarios.<id>] config id and is forwarded
to securities/expense/nii only. The loans runner's scenario is a projection-block
NAME inside the loans workbook's own MEV sheet — a different namespace — and
stays config-owned ([firm_data.loans].scenario); use run_loans.py --scenario
directly for a one-off override.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import importlib
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for _entry in (ROOT / "src", ROOT / "examples"):
    if str(_entry) not in sys.path:
        sys.path.insert(0, str(_entry))

from scb_ppnr.core.schemas import ValidationFailure  # noqa: E402
from scb_ppnr.ingestion.config import compose_config, load_config  # noqa: E402

STAGES = ("loans", "securities", "expense", "nii")
_STAGE_MODULES = {
    "loans": "run_loans",
    "securities": "run_securities",
    "expense": "run_from_config",
    "nii": "run_nii",
}
_STAGE_ARTIFACTS = {
    "loans": ("loans_report.txt", "loans_paths.csv"),
    "securities": ("securities_report.txt", "securities_paths.csv"),
    "expense": ("expense_report.txt",),
    "nii": ("nii_report.txt",),
}
SYNTHETIC_CONFIG = ROOT / "examples" / "synthetic_config.toml"
DEFAULT_COMPANY_MANIFEST = ROOT / "config" / "runs" / "company.toml"


@dataclass
class StageOutcome:
    stage: str
    status: str  # "ok" | "FAILED" | "skipped (<reason>)"
    exit_code: int | None
    seconds: float
    detail: str | None
    artifacts: list[str]


def _stage_argv(stage: str, args: argparse.Namespace, out: Path) -> list[str]:
    config = [] if args.config is None else ["--config", str(args.config)]
    scenario = [] if args.scenario is None else ["--scenario", args.scenario]
    if stage == "loans":
        # NO --scenario: the loans flag is a workbook MEV block NAME, not a
        # [mev.scenarios.<id>] id (see the module docstring's SCENARIO NOTE).
        return [*config,
                "--report", str(out / "loans_report.txt"),
                "--paths-out", str(out / "loans_paths.csv")]
    if stage == "securities":
        return [*config, *scenario,
                "--report", str(out / "securities_report.txt"),
                "--paths-out", str(out / "securities_paths.csv"),
                "--paths-basis", args.paths_basis]
    if stage == "expense":
        return [*config, *scenario, "--report", str(out / "expense_report.txt")]
    argv = [*config, *scenario, "--report", str(out / "nii_report.txt")]
    if args.config is not None:
        argv += ["--component-paths",
                 str(out / "loans_paths.csv"), str(out / "securities_paths.csv")]
    return argv


def _nii_missing_inputs(args: argparse.Namespace, out: Path) -> list[Path]:
    if args.config is None:  # demo mode uses run_nii's committed synthetic pair
        return []
    return [p for p in (out / "loans_paths.csv", out / "securities_paths.csv")
            if not p.exists()]


def _call(stage: str, argv: list[str]) -> tuple[int, str | None]:
    """Invoke one runner main() in-process; normalize every outcome to (rc, detail).

    Return conventions differ (run_loans/run_nii return int, run_securities
    returns None), run_securities raises SystemExit(str) on a missing [mev]
    and lets ValidationFailure propagate, and argparse exits with SystemExit(2)
    on a bad flag — all folded here, so the pipeline never dies mid-chain.
    """
    try:
        main_fn = importlib.import_module(_STAGE_MODULES[stage]).main
        rc = main_fn(argv)
    except SystemExit as exc:
        code = exc.code
        if code in (0, None):
            return 0, None
        if isinstance(code, int):
            return code, None
        print(f"\n{code}", flush=True)
        return 1, str(code)
    except ValidationFailure as exc:
        print(f"\nVALIDATION FAILURE — {exc}", flush=True)
        return 1, str(exc)
    except Exception as exc:  # ImportError (openpyxl), TOMLDecodeError, bugs
        traceback.print_exc()
        detail = f"{type(exc).__name__}: {exc}"
        if isinstance(exc, ImportError) and "openpyxl" in str(exc):
            detail += " — install with: pip install -e '.[excel]'"
        return 1, detail
    return (rc if isinstance(rc, int) else 0), None


def _manual_command(stage: str, argv: list[str]) -> str:
    return f"PYTHONPATH=src python3 examples/{_STAGE_MODULES[stage]}.py " + " ".join(argv)


def _run_stage(index: int, stage: str, args: argparse.Namespace, out: Path) -> StageOutcome:
    missing = _nii_missing_inputs(args, out) if stage == "nii" else []
    if missing:
        names = ", ".join(p.name for p in missing)
        return StageOutcome(stage,
                            f"skipped (missing {names}; run loans/securities into the same --out first)",
                            None, 0.0, None, [])
    argv = _stage_argv(stage, args, out)
    bar = "=" * 74
    print(f"\n{bar}\n=== [{index}/{len(STAGES)}] {stage}\n"
          f"=== {_manual_command(stage, argv)}\n{bar}\n", flush=True)
    started = time.monotonic()
    if args.quiet:
        log_path = out / f"{stage}.log"
        print(f"(--quiet: stage output -> {log_path})", flush=True)
        with open(log_path, "w", encoding="utf-8") as log, contextlib.redirect_stdout(log):
            rc, detail = _call(stage, argv)
    else:
        rc, detail = _call(stage, argv)
    seconds = time.monotonic() - started
    artifacts = [name for name in _STAGE_ARTIFACTS[stage] if (out / name).exists()]
    return StageOutcome(stage, "ok" if rc == 0 else "FAILED", rc, seconds, detail, artifacts)


def _dig(raw: dict, dotted: str):
    node = raw
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def _effective_config_text(config_path: Path) -> str:
    """key = value  # source-file, one line per leaf — the values complement to
    format_effective_config (which prints sources only). Used for --check and
    out/effective_config.txt so before/after config migrations can be diffed
    value-for-value."""
    raw, provenance = compose_config(Path(config_path))
    lines = [f"EFFECTIVE CONFIG WITH VALUES (key = value  # source) — {config_path}"]
    for key in sorted(provenance):
        value = _dig(raw, key)
        if isinstance(value, dict):
            continue  # table-level provenance entries; leaves only
        lines.append(f"{key} = {value!r}  # {provenance[key]}")
    return "\n".join(lines)


def _check(config_arg: Path | None) -> int:
    target = Path(config_arg) if config_arg is not None else SYNTHETIC_CONFIG
    label = "" if config_arg is not None else " (synthetic demo config — pass --config for yours)"
    try:
        config = load_config(target)
        text = _effective_config_text(target)
    except ValidationFailure as error:
        print(f"CONFIG CHECK FAILED — {error}", flush=True)
        return 1
    print(text + "\n", flush=True)
    if config.mev is not None:
        print(f"scenarios: {', '.join(config.mev.scenarios)}", flush=True)
    firm = config.firm_data
    present = [name for name, there in (
        ("spot+quarterly", firm is not None and firm.spot is not None),
        ("securities", firm is not None and firm.securities is not None),
        ("loans", firm is not None and firm.loans is not None),
    ) if there]
    print(f"firm sections: {', '.join(present) or 'none'}", flush=True)
    print(f"\nCONFIG OK{label} — composes and validates. Data files and the "
          f"TO_BE_CONFIRMED gates are checked at run time; drop --check to execute.",
          flush=True)
    return 0


def _write_effective_config(config_arg: Path | None, out: Path) -> str | None:
    target = Path(config_arg) if config_arg is not None else SYNTHETIC_CONFIG
    try:
        (out / "effective_config.txt").write_text(
            _effective_config_text(target) + "\n", encoding="utf-8")
    except Exception as exc:  # the stage itself will fail with the real diagnostic
        return f"effective_config.txt not written ({type(exc).__name__}: {exc})"
    return None


def _summary(outcomes: list[StageOutcome], out: Path, argv_text: str,
             note: str | None = None) -> tuple[str, int]:
    bar = "=" * 74
    lines = [f"\n{bar}", "RUN SUMMARY", bar]
    if note is not None:
        lines.append(f"  NOTE: {note}")
    width = max(len(o.status) for o in outcomes)
    for o in outcomes:
        timing = f"{o.seconds:6.1f}s" if o.exit_code is not None else "      -"
        arts = ", ".join(o.artifacts) if o.artifacts else "-"
        lines.append(f"  {o.stage:<10} {o.status:<{width}}  {timing}  {arts}")
        if o.detail:
            lines.append(f"  {'':<10} ^ {o.detail}")
    failed = [o.stage for o in outcomes
              if o.status != "ok" and o.status != "skipped (not selected)"]
    verdict = ("PIPELINE: OK — every selected stage green" if not failed
               else f"PIPELINE: FAILED (stages: {', '.join(failed)})")
    lines += [bar, verdict, f"artifacts in {out}", bar]
    text = "\n".join(lines)
    (out / "run_summary.txt").write_text(
        f"{argv_text}\n{text}\n\ngenerated {dt.datetime.now():%Y-%m-%d %H:%M}\n",
        encoding="utf-8")
    return text, 0 if not failed else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        epilog="Specialized/diagnostic runners stay available in examples/ "
               "(run_loans.py --retail-only, diagnose_securities.py, ...).")
    parser.add_argument("--config", type=Path, default=None,
                        help="config file or include-manifest (anything load_config accepts); "
                             "omit for the synthetic demo chain")
    parser.add_argument("--scenario", default=None,
                        help="[mev.scenarios.<id>] id for securities/expense/nii; the loans "
                             "scenario is config-owned (different namespace, see docstring)")
    parser.add_argument("--out", type=Path, default=None,
                        help="artifact directory (default out/<timestamp>/, gitignored)")
    parser.add_argument("--only", nargs="+", choices=STAGES, default=None,
                        help="run only these stages (canonical order is kept)")
    parser.add_argument("--paths-basis", choices=("xr", "full"), default="xr",
                        help="securities --paths-out basis passthrough (xr = reinvestment "
                             "excluded, PID-SEC-8)")
    parser.add_argument("--quiet", action="store_true",
                        help="stage output to out/<stage>.log instead of the terminal")
    parser.add_argument("--check", action="store_true",
                        help="compose + validate the config, print key = value  # source, "
                             "run nothing")
    args = parser.parse_args(argv)

    if args.check:
        return _check(args.config)

    out = (args.out if args.out is not None
           else ROOT / "out" / f"{dt.datetime.now():%Y%m%d-%H%M%S}")
    out = out.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    selected = tuple(s for s in STAGES if args.only is None or s in args.only)
    if args.config is None:
        print("SYNTHETIC DEMO CHAIN — each stage runs its own self-contained demo "
              "(invented data, hand-checkable numbers). Pass --config for a company run.",
              flush=True)
        if DEFAULT_COMPANY_MANIFEST.exists():
            print(f"NOTE: found {DEFAULT_COMPANY_MANIFEST.relative_to(ROOT)} — pass "
                  f"--config {DEFAULT_COMPANY_MANIFEST.relative_to(ROOT)} to run it.",
                  flush=True)
    note = _write_effective_config(args.config, out)

    outcomes: list[StageOutcome] = []
    for index, stage in enumerate(STAGES, start=1):
        if stage not in selected:
            outcomes.append(StageOutcome(stage, "skipped (not selected)", None, 0.0, None, []))
            continue
        outcomes.append(_run_stage(index, stage, args, out))
    text, rc = _summary(outcomes, out,
                        argv_text="run.py " + " ".join(argv or sys.argv[1:]),
                        note=note)
    print(text, flush=True)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
