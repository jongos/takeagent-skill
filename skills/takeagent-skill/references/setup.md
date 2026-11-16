# Connection and installation

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

Use HTTP MCP with JSON responses, OAuth authorization-code/S256 PKCE, resource binding and supported client registration. Resource: https://takeagent.ai/api/mcp. Discovery: https://takeagent.ai/.well-known/oauth-protected-resource/api/mcp and https://takeagent.ai/.well-known/oauth-authorization-server. Let the client handle token storage, refresh and expiry. Legacy SSE-only clients are not supported.

After connection, initialize, discover tools and call account.access. Verify a synthetic review without private data. Revocation is managed at https://takeagent.ai/account. After 401 reconnect through OAuth; after 403 explain current access/scope; after 429 stop until retry is permitted. Do not repeatedly retry or substitute credentials.

Platform instructions were researched November 16, 2026. Named-client end-to-end TakeAgent acceptance is not established by these instructions. Record client/version and actual results before calling it verified.
