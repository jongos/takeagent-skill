# takeagent-skill v0.1.1

Download **takeagent-skill.zip** and the matching SHA-256 receipt below.

- Checks the TakeAgent connection and account.access before account work.
- Reminds signed-out users: "Sign in to TakeAgent to use your account's access."
- Keeps signed-out/unknown accounts separate from verified Free and eligible accounts.
- Offers the EP suggestion only for an explicit authenticated plan restriction, at most once per session.
- Clears stale account permissions after expiry, reconnection or account changes; preserves reminder flags across session continuation.
- Aligns the landing page with the TakeAgent app's white, blue and DM Sans design.

Replace your previously installed skill with this ZIP. Installing instructions alone does not connect an account; complete OAuth in a compatible host. Behavior is implemented as portable agent instructions, with access enforced by TakeAgent's existing service. Named-client end-to-end acceptance remains pending.

Landing page: https://jongos.github.io/takeagent-skill/
