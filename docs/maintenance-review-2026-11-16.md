# Maintenance review — November 16, 2026

Source baseline: v0.1.5, commit `301e5689ed8d0eca06562db9358eaff5a474962a` (pre-merge snapshot).
This is a repository review, not a new release, deployment or client certification.

## Outstanding issue dispositions

| Reports | Change or finding |
|---|---|
| #16 / #19 | Marked the v0.1.2 security review explicitly historical; retained its original test counts, hash and observed page state instead of rewriting evidence. README now links this review for current dispositions. |
| #17 / #20 | Marked the v0.1.3 issue review explicitly historical; its live-page observation is not a claim about the current deployment. |
| #18 / #21 | Added the self-hosted fonts' SIL OFL license and direct license link beside MIT in the landing-page fine print. |
| #22 | Retained the explicit manual-only host/OAuth acceptance limitation and required it in release notes; packaging tests cannot certify vendor behavior. No live host tests claimed. |
| #23 | Added a pre-release and monthly manual revalidation cadence, with client/version evidence and untested status when access is unavailable. HTTP link checks alone cannot validate UI paths or OAuth. |
| #24 | No scanner replacement: CI already pins gitleaks 8.30.1 and verifies the archive's SHA-256 before extraction/execution. Replacing it with an action is not automatically safer; that action can download a binary too. Keep the checksum-pinned approach and review both version and digest on updates. |
| #25 | Source already writes each output via a same-directory temporary file and atomic replacement. Added success/failure cleanup and prior-file preservation regression tests. The pair is not a multi-file transaction, and remains unsigned; these limitations are not closed by the tests. |

## Validation boundary

Run the README build/check commands against the exact proposed commit and inspect CI before merging. The suite now contains 27 tests, including two atomic-write regressions and a landing-page license attribution check. This count is not a claim that tests passed in every environment. CI also checks version links, archive integrity and pinned-hash gitleaks scanning of history and expanded package. Release-event CI compares published assets against a tagged rebuild; it is not exercised by a pull request.

No changes to the packaged instruction files or VERSION are included. No new ZIP, release or production deployment is implied. Historical release digests are not replaced with unverified current values.

## Remaining release risks

- Named-client sign-in, expiry, revocation, owner isolation and behavioral acceptance still need synthetic, authorized client testing.
- An interrupted build between the two output replacements can leave an inconsistent ZIP/checksum pair. Rerun the build and verify `sha256sum --check takeagent-skill.zip.sha256` before uploading both outputs. Consumers must likewise verify the checksum before installation. Do not treat individual atomic writes as a two-file transaction.
- Checksums do not authenticate a publisher. Signing or attestation needs a separately reviewed release workflow and trust/verification policy; this change does not enable identity-token permissions or claim signed artifacts.