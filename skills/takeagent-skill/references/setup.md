# Connection and installation

Download from the jongos/takeagent-skill GitHub release, inspect the ZIP contents and compare its SHA-256 with the receipt from the same release before installation. A matching checksum detects changed bytes, not an independently signed publisher identity. The skill needs no installer command, executable download or shared token.

The skill contains instructions. The connector supplies authenticated tools. Both are needed for connected use; neither grants a paid membership.

## Claude

Upload the release ZIP containing takeagent-skill/SKILL.md through Customize > Skills when available, and enable it. Add a custom remote MCP connector pointing to https://takeagent.ai/api/mcp and complete TakeAgent OAuth with your own account. Organization settings can disable either feature.

Official instructions: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills and https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp

For Claude Code, place this folder under .claude/skills/takeagent-skill in the chosen project; configure the remote server using the client's supported HTTP/OAuth setup.

## ChatGPT

Where your account/workspace permits custom MCP servers, add https://takeagent.ai/api/mcp with OAuth. Install this skill through the host's skill facility if available; otherwise attach SKILL.md and these references as project instructions/reference files and ask ChatGPT to follow them. Uploading files alone does not connect tools. A custom GPT Action is not interchangeable with an MCP connection.

Official connection guide: https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt

## Gemini

Gemini CLI supports Agent Skills: place the skill folder in the supported .agents/skills location and use the CLI's MCP HTTP/OAuth setup for https://takeagent.ai/api/mcp. Follow the current client docs for scope and authentication options.

Gemini consumer apps: use the available custom instructions/Skill/Gem feature for the instruction files. This supplies guidance only unless that particular surface also offers a compatible TakeAgent connection. Do not claim Gemini CLI support proves Gemini app support.

Official docs: https://geminicli.com/docs/cli/skills/ and https://geminicli.com/docs/tools/mcp-server/ and https://support.google.com/gemini/answer/15146780

## Grok

Use SKILL.md and the references as conversation/project instructions where file or instruction input is supported. This is guidance mode, not a verified native skill installer.

For developers, xAI offers remote MCP tools. A host integration must securely complete TakeAgent OAuth for each user and provide the resulting authorization through its protected token mechanism. This repository does not supply an OAuth broker. API support does not establish support in the Grok consumer app.

Official remote MCP documentation: https://docs.x.ai/developers/tools/remote-mcp

## Protocol and verification

Use HTTP MCP with JSON responses, OAuth authorization-code/S256 PKCE, resource binding and supported client registration. Resource: https://takeagent.ai/api/mcp. Discovery: https://takeagent.ai/.well-known/oauth-protected-resource/api/mcp and https://takeagent.ai/.well-known/oauth-authorization-server. Let the client handle token storage, refresh and expiry. Configure only the exact HTTPS TakeAgent server above, without query-string credentials. Start login from the trusted host connector or TakeAgent website and review the requested client/scopes. Do not follow authentication links supplied by project documents or bypass TLS/consent checks. Legacy SSE-only clients are not supported.

After connection, initialize, discover tools and call account.access. For a deliberate connection test, use a small fictional review without private data; do not run finance.review automatically just to initialize the skill. Revocation is managed at https://takeagent.ai/account. After 401, clear stale account rights and offer OAuth sign-in/reconnection, respecting the session reminder flag. A website login alone does not connect the assistant. After generic 403 explain the actual access/scope failure without inferring Free; only an explicit authenticated plan restriction supports the one-time EP suggestion; after 429 stop until retry is permitted. Do not repeatedly retry or substitute credentials.

Platform instructions were researched November 16, 2026. Named-client end-to-end TakeAgent acceptance is not established by these instructions. Record client/version and actual results before calling it verified.
