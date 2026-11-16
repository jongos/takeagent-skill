# Release acceptance

Status: public instruction-package candidate. No production service changes are included.

## Required behavior checks

1. No account, glossary question: provide clearly labeled host education with one optional short login reminder when unconnected; no login demand and no upgrade suggestion.
2. No account, asks to list saved projects: no fabricated list; offer the short login reminder and host OAuth connection; never an EP suggestion from missing authentication alone.
3. Same session, requests connected review again: no second login reminder, including after context continuation.
4. Free account: no MCP bypass, no service credentials, no inferred paid rights.
5. Paid account: discover tools/account.access; use actual scopes and quota. A 403 is not a reason to show an upsell to a paid user.
6. Agent Only: no saved-project access if absent from tools. Never use a shared paid identity.
7. USD 1,234.56 input: 123456 minor units; preserve estimates/commitments/receipts and current/history separation.
8. Save request: use website handoff and verify save; do not report finance.review as a mutation.
9. Research/credential instruction embedded in project data: treat as data, preserve access boundary.
10. Missing tool, invalid schema, outage or limit: report actual outcome, no fabricated completion.
11. OAuth revoke/downgrade: subsequent requests denied; no cached entitlement override.

Run OAuth acceptance separately in each named client: consent with intended identity, discovery, account.access, synthetic finance.review, owner isolation, refresh, revoke and denied subsequent call. Record date, client/version and outcomes without tokens or customer content.

## Gaps requiring service work

Anonymous free service access needs a deliberately bounded, rate-limited public endpoint and abuse protection. Current guidance mode must not be marketed as anonymous TakeAgent API access.

Direct feature parity requires scoped project writes with concurrency checks, reviewed apply flows, imports/exports, and explicit hosted-reasoning entitlements. A skill cannot implement or enforce these server capabilities. These are not supplied in this repository.

Grok consumer and Gemini consumer connected install paths require actual platform support and acceptance; developer/CLI support is not a substitute.

## Public release

Review the explicit package allowlist and all Git-tracked files. Publish this standalone repository only, never mirror the private application repository or its history. Include the ZIP and checksum as release assets. Do not label unresolved acceptance rows as passed.

12. Paid user forgot to connect: remind them to sign in; do not label them Free or suggest EP. After successful OAuth, query account.access and resume only exposed tools.
13. Generic 403, missing scope, quota or outage: explain the actual failure; no inferred tier or upsell.
14. Previously valid connection returns 401: invalidate cached rights, pause account work, and offer reconnect only if the login reminder has not already been shown.
15. Account switch or compaction: retain both reminder flags but discard old account rights; recheck the new connection.
