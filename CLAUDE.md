@PROJECT_CONTEXT.md

# Core Working Rules

## Source hierarchy

1. The Federal Reserve PDF is authoritative.
2. The Markdown conversion is the primary searchable working source.
3. If an equation, table, variable name, footnote, or symbol may have been
   damaged during conversion, verify it against the corresponding PDF page.
4. Do not treat interpretations or coding proposals as Federal Reserve statements.

## Methodology rules

- Focus on the proposed 2026 PPNR methodologies identified in PROJECT_CONTEXT.md.
- Refer to the current 2025 models only when necessary for background or comparison.
- Never invent missing methodology.
- Mark unclear or unspecified information as UNKNOWN.
- Separate:
  - SOURCE-STATED FACT
  - INTERPRETATION
  - CODING CONSIDERATION
  - OPEN QUESTION
- Provide a PDF page number and Markdown section anchor for every material methodology claim.
- Preserve exact terminology from the source while also providing coding-friendly names.
- Clearly identify inputs, transformations, assumptions, parameters, intermediate calculations, and outputs.
- Clearly distinguish lift-off-quarter values from projection-quarter values.
- Record whether balances, portfolio composition, rates, or other variables remain constant over the projection horizon.

## Workflow rules

- Work on one bounded deliverable or model family at a time.
- Do not create the entire handbook in one pass.
- Do not write production Python during Phase 1.
- Begin substantive responses with a short summary.
- Before broad file changes, provide a plan and wait for approval.
- Ask no more than three questions when genuinely blocked.
- Put unresolved issues in handbook/open-questions.md.
- Do not silently overwrite approved handbook content.
- When reviewing a chapter, identify errors before proposing a rewrite.

## Confidentiality boundary

- No confidential Excel workbooks, screenshots, formulas, sheet names, data,
  internal paths, or firm-specific implementation details belong in this repository.
- The repository may contain only public Federal Reserve material, original
  nonconfidential documentation, generic specifications, and synthetic examples.