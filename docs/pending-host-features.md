# Pending host documentation (do not merge before production)

The branch `cursor/docs-pending-takeagent-features-0610` adds skill wording for TakeAgent behaviors that are staged but **not yet enforced in production**:

- **terms_acceptance_required** / Excel **terms_required** on MCP and companion surfaces
- **PDF export default** with **30 exports per rolling 24 hours** cap
- Hosted-assistant **PDF/Excel** uploads with **placementWarning** and hidden-content acknowledgement

Merge that PR only after the corresponding takeagent release ships and the behaviors are verified. The skill instructions state that Terms errors appear **only when the live server returns them**.