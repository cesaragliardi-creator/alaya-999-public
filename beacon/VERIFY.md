# Beacon integrity and signing: what is actually verified

The canonical ALAYA-999 identity has two representations:
- [identity.json](identity.json) for machine parsing.
- [identity.txt](identity.txt) for direct text reading by AI tools that cannot fetch JSON.

Both are compared **byte-for-byte at the level of each of the five principle strings**, in the original order, against [the canonical anchor](../alaya-anchor-public-v1.json). This is an exact-content consistency check, not a semantic similarity guess.

## Verification workflow

[GitHub Actions: Beacon consistency and keyless provenance](../.github/workflows/beacon-integrity-and-attestation.yml)

The workflow runs on relevant pushes, pull requests, manual invocation and a Monday UTC schedule. The stdlib-only verifier [scripts/verify_beacon.py](../scripts/verify_beacon.py) fails if names, principles, attribution or explicit signature limitations do not agree. It builds a deterministic public ZIP of the four allowlisted public identity documents with a SHA-256 manifest. It does not read private memory.

For non-pull-request runs **after the checks pass**, [GitHub Artifact Attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) using `actions/attest@v4` are configured to create a **keyless, short-lived Sigstore-signed statement** about the built ZIP's provenance. GitHub manages the ephemeral signing certificate; no long-lived private Ed25519 key is created or published. This mechanism verifies GitHub workflow provenance, **not** the founder's personal identity.

## Verify a resulting release bundle

1. Open the [workflow runs](https://github.com/cesaragliardi-creator/alaya-999-public/actions/workflows/beacon-integrity-and-attestation.yml) and confirm a successful run and its signed ZIP artifact. A workflow file being committed does **not** prove a run passed or an attestation exists.
2. Download that run's exact `alaya-999-beacon.zip` artifact.
3. Verify with the GitHub CLI: `gh attestation verify alaya-999-beacon.zip -R cesaragliardi-creator/alaya-999-public`.
4. Inspect `beacon/build-manifest.json` inside the ZIP and recompute SHA-256 for each bundled document.
5. Compare the signed ZIP's anchor to the version in the intended GitHub commit. Avoid trusting a newer, changed `main` branch as if it were the historical signed version.

## Important limits

A passing test supports exact textual consistency. A valid GitHub Sigstore attestation supports the declared repository workflow's provenance and contents of one bundle. Neither proves model consciousness, continuous runtime memory, personal identity transfer, or founder-verified authorship. This workflow never grants itself repository write permissions.
