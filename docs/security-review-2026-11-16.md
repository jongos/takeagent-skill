# Skill Review and Hardening — November 16, 2026

Scope: public skill instructions, installation guidance, release packaging and the static download page. No private backend or production authentication changes. This is a source review with packaging regression tests, not an independent penetration test or proof of behavior in every AI host.

## Findings and Fixes

| Finding | Impact | Fix |
|---|---|---|
| Account switches cleared permissions but did not explicitly invalidate project context | A host could reuse prior-account data in a later tool request | Invalidate selected IDs, cursors and cached results; require explicit authorization and fresh access verification before reuse |
| Tool names and pasted account responses were insufficiently distinguished from trusted connection state | Untrusted content could be mistaken for an entitlement | Bind access checks to the configured HTTPS TakeAgent connection; reject missing, conflicting or malformed account results |
| Browser handoff scope was too broad | Review could drift into saving, deletion, spending or external submission | Require the actual requested action/target, preserve unsaved work, reread ambiguous writes, forbid gate bypass |
| Project pagination lacked repeat/budget handling | A bad cursor could cause repeated calls and quota use | Detect repeated cursors, deduplicate and default to five pages; report partial coverage |
| Builder reread inputs after validation | The archive could contain bytes not actually validated | Read a bounded snapshot once and package those exact bytes |
| Builder accepted a local reference absent from its allowlist | Installed skill could contain broken references | Require local Markdown targets to exist in the packaged snapshot |
| Linked root/ancestor/output paths and unsafe link schemes needed stronger handling | Build could read/write outside its intended location | Reject symlink/reparse paths, escaping targets and non-HTTPS external Markdown links |
| Archive bytes depended on checkout line endings | Windows/Linux builds could disagree | Normalize text, pin archive metadata and verify exact archive contents |

## Validation

Twelve packaging tests cover allowlist-only output, checksum accuracy, newline reproducibility, unshipped/escaping/encoded references, unsafe link schemes, last-good preservation on invalid input, input size bounds, snapshot consistency, and linked input/root/output rejection.

Local Windows run: nine passed, three symlink cases skipped because the OS denies symlink creation. A pinned, read-only Linux GitHub Actions workflow runs the full suite and archive checksum verification. Its completed result must be verified before release; source configuration alone is not a passing CI claim.

The updated skill is checked with the skill-creator validator. Account/prompt branches were reviewed against the service contract; no fabricated host evaluation or live OAuth exercise is claimed.

## Remaining Limits

- A portable instruction file cannot enforce model compliance, session memory or account isolation. Server-side entitlements/ownership and host OAuth remain authoritative.
- Reminder flags are conversation state, not a persistent cross-client store. When prior display is uncertain, instructions suppress unsolicited repeats.
- Named-client sign-in, downgrade, revocation and cross-account behavioral acceptance remain pending.
- The builder assumes a trusted local checkout. It does not lock out concurrent hostile filesystem changes, authenticate publisher identity or certify that allowlisted prose contains no secrets. Review files before publication.
- Each output is replaced atomically, but ZIP/checksum are not a multi-file transaction. Always verify the checksum before upload and after download.
- Checksums detect byte changes; they are not signed provenance.
