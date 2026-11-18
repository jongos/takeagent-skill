# takeagent-skill v0.1.13

Documents live **finance.review** behavior on TakeAgent (host reference commit 87c247e, PR “Add lender versus equity needs to finance.review”), plus tier-accurate guidance for dashboard, export report, and recoupment lifecycle features:

- **Mezzanine** as a source type distinct from **Debt**.
- **investors[].linkedEquitySourceId** and optional **lenderNeedsChecklist** (CAMA vs deposit-account control as separate entered items; completion bond optional).
- **equityTerms**, **mezzanineTerms** (**juniorToSourceIds**, intercreditor status), and **waterfallPlacements**.
- **lenderEquityNeeds** response block: lender unbundling, checklist, **bondCoverage** (only when a bond is in the plan), investor–equity links, mezz intercreditor checklist, illustrative waterfall with deal-documents caveat.
- Prose uses **deficit** for budget-versus-sources shortfalls; **gap** reserved for gap financing against unsold sales estimates (JSON **projectedGap** / **committedGap** explained as deficit amounts).
- Completion bonds optional throughout—no “missing bond” flags.

Adds acceptance cases 51–56. No TakeAgent service code is included in this repository.

## Documentation (service features)

- **rebalanceSuggestions** in **finance.review**: advisory reconciled-coverage edits; not approval.
- **Project dashboard** and **export report**: **EP, Plus, and Pro**; not on Free or any Agent plan (Agent EP, Agent Plus, Agent Pro).
- **lifecycleChart** recoupment lifecycle and workspace **scenarios** (not forecasts): **Plus and Pro** only; omitted from **finance.review** on Free, EP, and all Agent plans. Scenario set covers baseline receipts at 1.3× cost, −30%, +30%, tax credit under expected, and custom. Map **owed** / **collected** / **distributed** to **scenarios[].tiers[].contractedOwedMinor**, **scenarios[].totalIllustrativeRevenueMinor**, and **scenarios[].tiers[].allocatedMinor**. Receipts are after exhibitor and distributor shares; off-the-top costs are not modelled yet; no tax-credit recourse modelled (per-loan recourse not yet available).
- **review.scenarios** funding stress in **finance.review**: still on all plans with **finance.review**.
- Tier-accurate upgrade reminders; **deficit** vs gap financing; completion bonds optional; whole-dollar display without trailing `.00`; illustrative examples labeled.