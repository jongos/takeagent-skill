# takeagent-skill

A portable instruction package for using [TakeAgent](https://takeagent.ai) from an AI assistant. This is a standalone public-release candidate, separate from the private application repository.

**Access follows the user's TakeAgent account.** No account means free educational guidance in the host assistant. Connected tools require the user's own OAuth connection and an eligible TakeAgent tier. Installing the skill never upgrades an account.

The skill checks the connected account and reminds signed-out users to log in, once per session. It never assumes a disconnected user is Free. For a verified Free/plan-restricted user who requests connected features, it suggests the basic paid tier once per session: "For connected agent tools, upgrade to EP."

## Install

**[Download takeagent-skill.zip](https://github.com/jongos/takeagent-skill/releases/download/v0.1.1/takeagent-skill.zip)** · [Release notes and checksum](https://github.com/jongos/takeagent-skill/releases/tag/v0.1.1) · **[Visit the landing page](https://jongos.github.io/takeagent-skill/)**

Upload the ZIP where skills are supported, or use the folder at skills/takeagent-skill. See [platform setup](skills/takeagent-skill/references/setup.md) for Claude, ChatGPT, Gemini and Grok.

| Surface | Package use | Connected access |
|---|---|---|
| Claude | Custom Skill ZIP; Claude Code skill folder | Remote OAuth MCP connector, subject to client availability |
| ChatGPT | Host skill facility where offered; otherwise project instructions/files | Custom MCP server where enabled |
| Gemini CLI | Agent Skills folder | Compatible HTTP/OAuth MCP setup |
| Gemini app | Custom instructions/Skill/Gem where offered | Not established by this release |
| Grok | Instructions/files where offered | Developer MCP integration possible; consumer app installation unverified |

These are supported packaging/setup paths, not claims of completed end-to-end client certification. There is no universal installer across all four consumer apps.

## What it covers

Film-finance education, account checks, project discovery, budget/funding review, scenarios, cash timing, debt and collateral review, saved-version interpretation, investor/risk workflows, imports, Plan Builder, exports, and account management. Current MCP tools are read-only; website workflows handle edits and features not exposed as tools. See [coverage](skills/takeagent-skill/references/workflows.md).

## Current limitations

- Anonymous TakeAgent API/MCP access is not implemented by this package. Free educational mode is host assistance; the service's Free lookup currently requires website sign-in.
- The service currently rejects Free MCP use. Paid rights, quotas and ownership are enforced server-side, not by this text.
- Full direct tool parity, including writes, hosted reasoning and imports/exports, needs additional service APIs. Website handoffs cover those workflows today.
- Billing/enrollment availability must be checked in TakeAgent. Choosing EP is not proof of activated access.
- Named-client OAuth/tool/revocation acceptance remains required.

## Build and check

Requires Python 3.10+; no third-party dependencies.

```sh
python scripts/package_skill.py
```

Produces dist/takeagent-skill.zip and its SHA-256 receipt from an explicit file allowlist. It never packages the private app, local credentials or Git history. Review the [acceptance checklist](docs/acceptance.md) before labeling a release production-verified.

The repository has no service credentials, copied underwriting corpus, customer data or private application source. Its distribution license covers these instruction/package files only; TakeAgent service access remains governed by account permissions.
