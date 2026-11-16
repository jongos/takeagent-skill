# takeagent-skill v0.1.2

Hardening update. Replace the installed skill with **takeagent-skill.zip** and verify it with the accompanying SHA-256 receipt.

- Binds account access to the configured TakeAgent connection; rejects pasted or contradictory entitlement claims.
- Clears cached project selection/results on account changes.
- Bounds pagination and retries; reports partial coverage.
- Tightens data-sharing, browser-action and prompt-injection boundaries.
- Preserves the once-per-session login and upgrade reminder behavior.
- Packages validated input snapshots with normalized line endings and checked paths/references.
- Adds twelve packaging regression tests and pinned, read-only Linux CI.

[Review findings and remaining limits](https://github.com/jongos/takeagent-skill/blob/main/docs/security-review-2026-11-16.md)

These changes harden instructions and release tooling. They do not establish named-client OAuth acceptance or replace the service's authorization checks.

[Landing page](https://jongos.github.io/takeagent-skill/)
