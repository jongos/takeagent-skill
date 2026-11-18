# takeagent-skill v0.1.13

**Unpublished.** Source and `VERSION` are at 0.1.13; the installable GitHub release asset is not published yet. Until publication, download links use [releases/latest](https://github.com/jongos/takeagent-skill/releases/latest) (currently v0.1.11 or later published tag).

Documents live **finance.review** behavior on TakeAgent (host reference commit 87c247e, PR “Add lender versus equity needs to finance.review”):

- **Mezzanine** as a source type distinct from **Debt**.
- **investors[].linkedEquitySourceId** and optional **lenderNeedsChecklist** (CAMA vs deposit-account control as separate entered items; completion bond optional).
- **equityTerms**, **mezzanineTerms** (**juniorToSourceIds**, intercreditor status), and **waterfallPlacements**.
- **lenderEquityNeeds** response block: lender unbundling, checklist, **bondCoverage** (only when a bond is in the plan), investor–equity links, mezz intercreditor checklist, illustrative waterfall with deal-documents caveat.
- Prose uses **deficit** for budget-versus-sources shortfalls; **gap** reserved for gap financing against unsold sales estimates (JSON **projectedGap** / **committedGap** explained as deficit amounts).
- Completion bonds optional throughout—no “missing bond” flags.

Adds acceptance cases 51–56. No TakeAgent service code is included in this repository.