# takeagent-skill v0.1.3

Issue-review fixes and reproducible release validation. Replace your installed skill with **takeagent-skill.zip** and verify the accompanying SHA-256 receipt.

- Reconnect help remains available after token expiry without repeating the one-time login prompt.
- Website handoff is the default; requested browser assistance is limited to relevant TakeAgent pages and minimal page data.
- EP and Agent Only are defined inside the downloadable package.
- Host-memory and prompt-enforcement limitations are explicit, with visible-thread checks and conservative reminder suppression.
- Metadata uses safe YAML parsing; Markdown links use a parser that understands references and code blocks.
- VERSION controls README and landing-page release links; CI detects drift.
- Release CI compares the uploaded ZIP/checksum against a rebuild from the tagged source.
- Mobile navigation keeps Set Up visible; documentation clarifies build dependencies and font licensing.

The regression suite now has 24 tests. Named-client behavioral/OAuth acceptance remains pending; portable instructions are not executable security controls.

[Landing page](https://jongos.github.io/takeagent-skill/) · [Issue disposition](https://github.com/jongos/takeagent-skill/blob/main/docs/issue-review-2026-11-16.md)
