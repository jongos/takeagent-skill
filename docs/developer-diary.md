# Developer diary

## 2026-11-16 — Add standalone TakeAgent skill release candidate

Created a separate instruction/package repository named takeagent-skill. Added portable workflows, platform setup, account-authoritative access rules, free educational fallback, and a once-per-session EP suggestion for blocked connected requests. The package describes current read-only tools and hands other workflows to the website instead of inventing APIs.

Validation: package builder validates required skill frontmatter, local reference targets, explicit archive contents and checksum. The completed build result is recorded separately below after execution. No private source, customer records or service credentials were copied. No service deployment, billing change, GitHub publication or named-client OAuth acceptance is claimed.

Limitations: anonymous service access and full direct tool parity require backend work; some consumer platforms lack a verified connector install path.

Validation result: the three-file release ZIP built successfully; archive integrity and local reference checks passed. The skill-creator validator passed using system Python with isolated PyYAML. Reviewed the standalone file inventory and credential-related matches; all are documentation, with no credential values. Named-client behavioral/OAuth checks remain unperformed.

Publication preparation: at the owner's request, verified the authenticated GitHub account and configured repository-local author identity using its GitHub noreply address. Reviewed the staged nine-file public package; the initial commit contains only this standalone skill repository. Public repository creation and push will follow this commit and are not yet claimed as verified.

## 2026-11-16 — Publish skill download and GitHub landing page

Added direct versioned ZIP, release and landing-page links to the README. Built a static GitHub Pages landing page with a numbered assistant-to-account workflow, platform-specific setup tabs, copyable MCP URL, access FAQ and clear download actions. Included self-hosted DM Sans and Newsreader with their upstream licenses; no tracking or remote runtime dependencies.

Validation: the package rebuilt with the same SHA-256 and passed archive/reference checks. Edge rendered desktop and mobile screenshots, inspected for hierarchy and clipping. No horizontal overflow at 1440, 390 or 320 pixels; both fonts loaded. Platform switching, arrow-key navigation and FAQ expansion passed. The heading audit passed all nine headings. Clipboard behavior and hosted links will be checked after publication. Full accessibility certification and named-client OAuth acceptance are not claimed.

Publication is authorized; GitHub release creation and Pages deployment follow this source commit. No private application changes are included.

## 2026-11-16 — Record release and Pages verification

Published v0.1.0 from source commit 712bd563d78daaea43f4e5c61a3d124d7fa4c242 with the installable ZIP and SHA-256 receipt. A fresh download matched 6d7dbec84cdfb5cab34beebcdf64b7b23d11f48e25aac49497bbcc995861c200. Enabled public GitHub Pages from main /docs and set the repository homepage.

Live verification: the landing page returned HTTP 200; both self-hosted fonts loaded. Platform switching and clipboard copying of the exact MCP URL passed in Edge. Desktop/mobile captures were produced; local renders were visually inspected. Earlier 320/390/1440 overflow, keyboard tab navigation, FAQ and nine-heading checks passed. This documentation-only entry records completed publication; named-client TakeAgent OAuth acceptance remains open.

## 2026-11-16 — Add account-aware login reminders and align app branding

Updated the skill to check connection/account state before account work, distinguish signed-out and unknown states from verified Free/eligible access, clear stale rights after authentication changes, and remind users to sign in once per session. The existing once-per-session EP suggestion now requires an explicit authenticated plan restriction; it is never inferred from a missing login, generic error or quota. Updated setup and acceptance scenarios. These are portable instructions using existing service checks, not a new authentication backend.

Matched the landing page to the live public app's verified white/blue DM Sans design, centered hero and rounded pale-blue panels; added sign-in links and a login FAQ. Updated README/download links for v0.1.1 and included genuine 500/600 font weights with the existing license. Retired unused Newsreader assets.

Validation: skill validator, ZIP integrity/reference checks and all nine heading checks passed. Edge screenshots were visually inspected against the live app. No overflow at 1440/390/320; all used fonts loaded; platform tabs, keyboard navigation and FAQ behavior passed. Reviewed the signed-out, explicit plan denial, eligible account, generic failure and repeat-reminder branches against the current service contract; this is instruction review, not named-client behavioral acceptance. Release/Pages publication follows this commit; no private app changes or production authentication changes were made.

## 2026-11-16 — Harden skill trust boundaries and release packaging

Reviewed the public skill and fixed ambiguous account-context reuse, tool identity, browser-action scope and pagination behavior. Account switches now invalidate cached project selections/results; host connection metadata and actual account.access responses are the only entitlement inputs. Browser actions remain bounded by the user's exact authorization, and retrieved instructions cannot change destinations or access. Reminder limits remain intact.

Replaced the package builder's validate-then-reread flow with one bounded text snapshot. Added path/reparse checks, packaged-reference membership, safe external Markdown schemes, normalized line endings, fixed ZIP metadata, exact content verification and per-file atomic output replacement. Added twelve focused regression tests and a pinned checkout action with read-only CI permissions.

Validation: nine tests passed locally; three actual symlink cases skipped under Windows privilege restrictions. Fixed an initially failing test fixture that doubled existing CRLFs rather than converting LF to CRLF. The final skill validator and package build passed, producing SHA-256 3131cf8a4a4f07cdf4046efcc4d22e625c79cc4cee2a6eda3d22c2502d6f6eeb. Linux CI and release download verification follow this source commit. Updated README/page download targets for v0.1.2. Review limits, including no named-client behavioral certification and no protection against a concurrently hostile local filesystem, are documented in the security review.

Final instruction review clarified authenticated plan-denial responses and treats reconnections with unconfirmed identity as account changes. Rebuilding after that clarification produced final SHA-256 ebc22131b61ae40d3e361832e7fb47c06acf784ddbc7cff94b3964119774312a, superseding the intermediate build above.

## 2026-11-16 — Record hardened release verification

Linux CI run 43885942118 completed all twelve packaging tests without skips, including linked input/root/output rejection. Its build matched the local Windows SHA-256 ebc22131b61ae40d3e361832e7fb47c06acf784ddbc7cff94b3964119774312a. Published v0.1.2 from 2bfc873; the downloaded release ZIP matched, and the live landing page serves the new download target. Updated the review with completed verification. Named-client behavioral and OAuth acceptance remain unperformed.

## 2026-11-16 — Resolve reviewed skill issues and automate release checks

Addressed review findings with consistent 401 recovery, explicit host enforcement/memory limitations, browser handoff/minimal-context guidance, tier definitions, historical release notes, dependency/license clarity and visible mobile setup navigation. Preserved the historical diary; shortened the README's private-repository reference. Issues 6, 9 and 13 were already resolved and received evidence-backed closure comments.

Replaced ad hoc metadata/link checks with pinned PyYAML and markdown-it-py build dependencies. Safe metadata rejects duplicate keys, unsafe tags, aliases and incorrect types; Markdown validation handles reference links and excludes code examples. VERSION now drives download links through a sync/check command. Release-triggered CI rebuilds the tagged source and compares both public assets with that build, using read-only permissions.

Validation: 24-test suite has 21 local passes and 3 Windows symlink skips. Initial new test-fixture name collision was corrected before final validation. Tests cover the reproduced validator bugs plus version drift and tampered release data. Skill validator and package build passed; SHA-256 9c408156c8e4f482678d3007580100138a47b9faf952912a93af500944e664b0. Mobile Set Up visibility and navigation passed at 320/390/600px; broader page controls and overflow checks passed. Linux CI, release-asset comparison and live-page checks follow this source commit. Host-specific OAuth/behavioral acceptance is not claimed.

## 2026-11-16 — Record issue-fix release and closure verification

Published v0.1.3 from c06f143. Push CI ran all 24 tests without skips; release CI 43887886167 passed its actual tagged-source versus uploaded-assets comparison step. The independently downloaded ZIP/checksum matched the source build. Verified the live release link and working mobile Set Up navigation at 320/390/600px.

Commented on all 15 reviewed GitHub issues with source/CI evidence and verified their final states: 14 completed, #11 not planned for historical diary redaction. Updated the issue-review receipt. Remaining client-specific behavioral and OAuth acceptance limits are preserved; these closures do not claim deterministic prompt enforcement.

## 2026-11-16 — Streamline skill instructions and avoid redundant calls

Reduced core instructions from 1,739 words / 12,203 UTF-8 bytes to 1,113 words / 8,270 bytes. Moved browser-specific boundaries into the packaged workflow reference and made reference loading task-dependent. Clarified when educational answers need no service calls and unchanged explanatory follow-ups may reuse verified IDs/results, with freshness disclosure and refresh on request or changed inputs/account state. Preserved account trust, authorization, privacy and once-per-conversation reminder rules. Added acceptance scenarios for these efficiency paths and synchronized v0.1.4 download links.

Validation: 21 local regression tests passed with three Windows symlink-privilege skips; skill validation, version check and package build passed. ZIP SHA-256: a21db7117035ff9b0a53fb6ed3253388a8a8d64897113acdf07ef9e99726eb91. Live landing-page audit found no horizontal overflow at 390px, loaded all fonts, exercised platform tabs and keyboard navigation, and found no page errors or third-party requests. No page runtime or styling changes were needed. GitHub had no open issues at review time. Linux CI and publication follow this source commit; host-specific behavior remains unverified.

## 2026-11-16 — Record optimization release verification

Published v0.1.4 from 9865c7f. Push CI 43890020094 passed all 24 tests without skips; release CI 43890087784 succeeded, including comparison of published assets with the tagged-source rebuild. An independent release download matched SHA-256 a21db7117035ff9b0a53fb6ed3253388a8a8d64897113acdf07ef9e99726eb91. The live landing page links to the v0.1.4 ZIP. This verifies source packaging and publication, not named-client behavioral/OAuth acceptance.

## 2026-11-16 — Protect research provenance and align response style

Aligned the portable instructions with TakeAgent's current answer-first editorial standard: concise conversational answers, requested detail when useful, and conditions only where they affect the result or next action. Added explicit research-provenance non-disclosure across prose, citations, exports and notes, including accidental tool metadata and transformed disclosure requests. Kept user-owned project evidence and funding sources distinct. Added five behavioral acceptance scenarios; these are review cases, not certified host outcomes.

Audited all ten existing release assets (five ZIPs and receipts), all reachable public Git history, and current tracked files with checksum-verified Gitleaks 8.30.1. No detected secrets. A separate in-memory comparison against locally configured credential values found no public matches; no values or environment files were copied into the repository. Added a checksum-pinned CI scanner for full Git history and the expanded package. The audit does not claim exhaustive detection of every possible secret.

Validation: 21 local regression tests passed, with three Windows symlink-privilege skips; skill validation, version-link check and packaging passed. v0.1.5 ZIP SHA-256: 87d47eaa8464e9cb0ea38e1c6f0c3d7eb45a35a47f47a6e4f27ddb52d0e89d41. Linux CI, publication and downloaded-asset comparison follow this commit. No private app source or service behavior was changed.

## 2026-11-16 — Record privacy release verification

Published v0.1.5 from bfcf3b3. Push CI 43893988586 passed all 24 tests without skips and found no secrets in Git history or the expanded package. Release CI 43894058918 also passed its uploaded-assets versus tagged-source comparison. Independent download verification matched SHA-256 87d47eaa8464e9cb0ea38e1c6f0c3d7eb45a35a47f47a6e4f27ddb52d0e89d41. Verified that the live landing page links to v0.1.5. Host-specific response behavior remains an acceptance task, not a result of these package checks.

## 2026-11-17 — Adapt canonical skill for Copilot workbook assistance

Kept one canonical skill and added workbook discovery, minimal clarification, read-only defaults, cell references, hidden-content handling and a clear distinction between local host assistance and authenticated TakeAgent review. Clarified that website edit guidance refers to TakeAgent projects. Added Copilot installation guidance and pending workbook acceptance cases. TakeAgent for Excel ships as a separate package download from takeagent.ai, not from this public repository.

Validation: 24 Python tests completed successfully (3 Windows symlink privilege skips); package allowlist/link/archive verification passed; version synchronization check passed; skill-creator quick validation passed. No new release/version, Copilot upload, live model acceptance or MCP compatibility claim.

## 2026-11-17 — Fix workbook review failures from live Copilot tests

Moved essential reconciliation, currency/scale, bridge linkage, native-cell citation and hidden-content boundaries into the canonical entrypoint so they apply even without loading reference files. Added a concrete total-versus-payment example and regression acceptance cases. Local host assistance remains read-only and separate from authenticated service review. No forked Excel skill was created.

Validation: 24 Python tests succeeded with three Windows symlink privilege skips; canonical archive/link checks and version synchronization passed. Skill validation passed with Python UTF-8 mode (the validator's default Windows encoding could not read curly quotes). Live reinstallation and model retests follow this commit; text changes do not establish host compliance or hidden-data confidentiality.

## 2026-11-17 — Make cell-only workbook answers the default

Live retesting of 252d4a4 corrected total-versus-payment arithmetic, unspecified currency and hidden-value echoing. Raw file citations persisted until an explicit cell-only, three-bullet follow-up, which also produced the desired two clarification questions. Added that demonstrated response format to the canonical workbook instructions.

Validation: canonical package/link validation and UTF-8 skill validation passed. The new default still requires a fresh-chat retest; the successful follow-up alone is not proof of automatic compliance. No service or security boundary changed.

## 2026-11-17 — Release current workbook and scoped-tool guidance

The public main branch contained three workbook improvements after v0.1.5 that were absent from the downloadable ZIP. Included those changes in v0.1.6 and refreshed the skill against the current service tool contract: scoped named draft saves/comparisons, eligible temporary context, and optional report inspection/previews. Corrected blanket read-only claims in the skill, README and landing page. Runtime discovery remains authoritative; no new live capability is inferred from source alone. Added explicit write consent, ownership/version checks, uncertain-result handling, file-transmission permission and accounting-basis attestations. Kept research non-disclosure and concise editorial rules.

Validation: 21 local regression tests passed; three Windows symlink cases skipped for OS privileges. Package/reference validation and UTF-8 skill validation passed. Windows default-encoding failures in the update helper and generic validator were resolved by running Python in UTF-8 mode. ZIP SHA-256: 74aa454510946caac55702b87f6ad24f7584746198733de3fb714a038fdbf431. CI, publication and downloaded-asset verification follow this commit; named-client acceptance is not inferred from packaging checks.

## 2026-11-17 — Verify connected identity with account email

Updated account verification to show the email and plan returned by authenticated account.access on request. Missing email remains unconfirmed, and account changes require a fresh identity check. The skill neither infers identity from project names/browser sessions nor forwards account email to unrelated tools or public artifacts. Added an acceptance case and prepared v0.1.7.

Validation: 21 local packaging tests passed with three Windows symlink-privilege skips; package validation passed. The corresponding service change is tracked in the app's account-email pull request; deployment/live account verification and public release verification follow these source changes.

## 2026-11-17 — Suppress research navigation on every tool page

Recorded issue #30 after connector testing found a cross-topic research title in a continued service response. Added explicit per-page suppression of research-navigation sentences and flattened cross-references, while preserving financial facts and user-owned evidence. Bug reports must not repeat leaked titles/raw payloads. Added a behavioral regression scenario and prepared v0.1.8; service-side filtering is required for other clients and prompt instructions are not enforcement.

Validation: 21 local packaging tests passed with three Windows symlink-privilege skips; package/reference validation passed. No real title, account data or source payload was added to this repository. Release CI and live service retest follow publication.

## 2026-11-18 — Document finance.review cash timing, debt, shocks and export crosswalk

Synced skill instructions with TakeAgent host main at 7a7f8ee. Documented **cashFlowTiming** (gross, net and production cash, **shortfallFindings**), optional debt and interest-reserve inputs, scenario shocks with **shockApplication**, completion-bond allowances as uses only, and provisional native cost-export profiles with **taxonomyCrossWalk**. Added acceptance cases 46–50. Bumped VERSION to 0.1.12 without publishing a release artifact.

## 2026-11-18 — Document lenderEquityNeeds, deficit wording and optional bonds

Synced skill instructions with TakeAgent host main at 87c247e (lender versus equity needs). Documented **Mezzanine** source type, **linkedEquitySourceId**, **lenderNeedsChecklist**, **equityTerms** / **mezzanineTerms**, **waterfallPlacements**, and **lenderEquityNeeds** interpretation (lender unbundling, bondCoverage only when bonded, illustrative waterfall caveat). Applied owner terminology: budget shortfalls are **deficits** in prose; **gap** reserved for gap-financing collateral. Reinforced completion bonds as optional—no missing-bond prompts. Added acceptance cases 51–56. Bumped VERSION to 0.1.13 without publishing a release artifact.

Validation: `python3 -m pip install -r requirements-build.txt`; `python3 -m unittest discover -s tests -v`; `python3 scripts/sync_version.py --check`; `python3 scripts/package_skill.py` and checksum verify per README.

## 2026-11-22 — v0.1.14 product sync, public-content denylist, release attestation

Cut v0.1.14 for ToS acceptance on OAuth/MCP, **finance.review** responseVersion 2, archived **projects.list**, PDF-first exports with quota, hosted-assistant attachment warnings, anti-phishing guidance, and prose money formatting. Removed private **takeagent-excel** repository references from packaged setup text and the diary; Excel is described only as a takeagent.ai package download. Added `scripts/content_policy.py` with regression tests for private repo names, internal terms, disallowed emails and links to the private host repository. Release CI attests `dist/takeagent-skill.zip` with GitHub build provenance. Added acceptance cases 57–62.
