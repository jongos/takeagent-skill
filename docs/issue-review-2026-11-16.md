# Issue Review — November 16, 2026

> Historical snapshot: the publication and live-page observations below describe v0.1.3 at the time of that release, not the current deployment. See [current validation and issue dispositions](maintenance-review-2026-11-16.md) and [VERSION](../VERSION).

Reviewed issues 1–15 against v0.1.2, then implemented the following v0.1.3 changes. Issue comments link the relevant commits and CI evidence after publication.

| Issue | Disposition |
|---|---|
| #1 | Clarified prompt-only versus server/host enforcement in README, skill, setup and acceptance. No claim of deterministic host enforcement. |
| #2 | Default website handoff; browser help only for a requested task, relevant TakeAgent pages and minimal visible context. |
| #3 | Align skill, setup and acceptance: always explain recovery after 401; never repeat the canned reminder. |
| #4 | Define conversation/thread scope, check visible history, suppress reminders when state is uncertain, explain host-specific memory limits. |
| #5 | Retain v0.1.2 CI; add VERSION synchronization/checks and release-tag rebuild comparison against uploaded assets. |
| #6 | Already fixed in v0.1.2: regression tests and successful Linux CI. |
| #7 | Safe YAML parser with unique keys/type validation and CommonMark-aware reference/code handling; regression cases added. |
| #8 | Define EP and Agent Only inside SKILL.md. |
| #9 | Already fixed in v0.1.2: all behavioral cases precede release guidance. |
| #10 | Add a historical supersession note to v0.1.0 notes without rewriting the original account of that release. |
| #11 | Shorten the README introduction; preserve the required historical developer diary. No credentials or private records were identified by this issue. Historical diary removal is not planned. |
| #12 | Keep Set Up visible and usable on mobile through a wrapping navigation row. |
| #13 | Already fixed in v0.1.2: package the single validated snapshot. |
| #14 | Document pinned build dependencies and commands; clarify that the previous external skill-creator check was supplementary. |
| #15 | Summarize MIT versus DM Sans SIL OFL licensing in README, linking both licenses. |

## Validation and Limits

Local regression suite: 21 passed, 3 symlink tests skipped by Windows privilege restrictions. Linux CI must run all 24 before release acceptance. Cases reproduce malformed YAML, duplicate keys/types, reference-style destinations, code examples, version drift, wrong tags and tampered release assets.

The mobile setup link passed at 320/390/600px; 1440/390/320px layouts, tabs/keyboard, font loading and FAQ controls passed. Rendered mobile navigation was inspected.

These fixes resolve the documentation and packaging findings. They do not implement vendor-specific policy middleware or certify host-model behavior. Follow docs/acceptance.md for named-client behavioral testing. Generic private-repository mentions and honest validation history are not credentials or evidence of a security breach.

## Completed Publication and Issue Disposition

All 24 tests passed without skips in Linux push CI [43887789728](https://github.com/jongos/takeagent-skill/actions/runs/43887789728). Release-event CI [43887886167](https://github.com/jongos/takeagent-skill/actions/runs/43887886167) successfully rebuilt the v0.1.3 tag and compared both downloaded release assets. An independent local download also matched SHA-256 9c408156c8e4f482678d3007580100138a47b9faf952912a93af500944e664b0.

The live page points to v0.1.3, and its Set Up navigation was verified at 320/390/600px. Issues 1–15 each received an evidence-backed comment: 14 were closed as completed; #11 was closed as not planned for the remaining historical-diary redaction suggestion. Host-specific behavioral/OAuth testing remains a documented acceptance gap, not a claimed implemented control.
