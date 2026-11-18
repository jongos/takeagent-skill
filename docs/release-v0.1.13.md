# takeagent-skill v0.1.13

**Unpublished.** Source and `VERSION` are at 0.1.13; the installable GitHub release asset is not published yet. Until publication, download links use [releases/latest](https://github.com/jongos/takeagent-skill/releases/latest) (latest **published** release is v0.1.8).

Documents live **finance.review** behavior on TakeAgent (host reference commit 87c247e, PR “Add lender versus equity needs to finance.review”):

- **Mezzanine** as a source type distinct from **Debt**.
- **investors[].linkedEquitySourceId** and optional **lenderNeedsChecklist** (CAMA vs deposit-account control as separate entered items; completion bond optional).
- **equityTerms**, **mezzanineTerms** (**juniorToSourceIds**, intercreditor status), and **waterfallPlacements**.
- **lenderEquityNeeds** response block: lender unbundling, checklist, **bondCoverage** (only when a bond is in the plan), investor–equity links, mezz intercreditor checklist, illustrative waterfall with deal-documents caveat.
- Prose uses **deficit** for budget-versus-sources shortfalls; **gap** reserved for gap financing against unsold sales estimates (JSON **projectedGap** / **committedGap** explained as deficit amounts).
- Completion bonds optional throughout—no “missing bond” flags.

Adds acceptance cases 51–56. No TakeAgent service code is included in this repository.

## Documentation (service features)

- **rebalanceSuggestions** in **finance.review**: advisory reconciled-coverage edits; not approval.
- **Project dashboard** and **export report**: **EP, Plus, and Pro**; not Free or Agent Only without dashboard access.
- **lifecycleChart** recoupment lifecycle and workspace **scenarios** (not forecasts): **Plus and Pro** only; omitted from **finance.review** on EP and lower. Scenario set covers baseline receipts at 1.3× cost, −30%, +30%, tax credit under expected, and custom. Revenue reads as receipts to the collection account; **owed**, **collected**, and **distributed** are separate lines; off-the-tops are not modelled; tax-credit lender defaults to non-recourse.
- **review.scenarios** funding stress in **finance.review**: still on all plans with **finance.review**.
- Tier-accurate upgrade reminders; **deficit** vs gap financing; completion bonds optional; whole-dollar display without trailing `.00`; illustrative examples labeled.