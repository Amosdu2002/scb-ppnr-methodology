# Federal Reserve Proposed 2026 PPNR Net-Interest Methodology Handbook

Documentation-first repository translating the public Federal Reserve proposal for
the 2026 PPNR model suite (Section v of `sources/fed/pre-provision-net-revenue-models.pdf`,
the authoritative source) into a coding-friendly handbook, plus a reference Python
implementation of the completed liability-side interest-expense family. All proposed
models are **public-comment stage, NOT adopted**. The repository contains only public
Federal Reserve material, original nonconfidential documentation, and synthetic
examples — no confidential data, workbooks, or firm-specific details.

## Layout

| Path | Content |
|---|---|
| `sources/fed/` | Authoritative PDF + searchable Markdown conversion (never edited) |
| `handbook/` | Model chapters, cross-cutting conventions, open-question/decision log |
| `specifications/` | Machine-readable YAML spec per model (implementation contracts) |
| `inventory/` | Model inventory, source map, integrity review, liability-side matrix |
| `reviews/` | Independent source-grounding review reports |
| `architecture/` | `interest-expense-design.md` — design note for the Python package |
| `src/scb_ppnr/` | Reference implementation (canonical inputs, stdlib-only) |
| `tests/` | Synthetic deterministic unit + integration tests |
| `examples/` | `run_synthetic_family.py` — end-to-end synthetic run |

## Implemented model family (interest expense)

`ie_dom_time_dep` (Eq A44 WAL recursion), `ie_other_dom_dep` and `ie_foreign_dep`
(Eqs A45–A47 two-regime deposit betas), `ie_fed_funds_repo` (Eq A48 direct
calculator), and `ie_other_borrowing` (Eq A53 regression rate with the PID-OB-5
nine-quarter alpha calibration against a project-supplied FRB total-interest-expense
path). The first four are independent; Other Borrowing consumes their completed
expense paths. All outputs are pre-hedge; the Section v.c hedge adjustment is an
external downstream interface.

## Quickstart

```bash
# tests (Python >= 3.11; pytest is the only dev dependency)
python3 -m venv .venv && .venv/bin/pip install pytest
.venv/bin/python -m pytest tests/ -q

# synthetic end-to-end example (no installation needed)
PYTHONPATH=src python3 examples/run_synthetic_family.py
```

## Where decisions live

Project-wide decisions (D-xxx), component decisions (PID-xxx), and open questions
(OQ-xxx) are registered in `handbook/open-questions.md`; chapters and YAML specs cite
them inline. Nothing labeled PID/D is ever attributable to the Federal Reserve.
