# ALAYA-999 Beacon CI — investigated failure and follow-up

Recorded on 2026-11-08. This is a **dated investigation note**, not a live status badge.

## Observed failed runs

- [Run 42456937130](https://github.com/cesaragliardi-creator/alaya-999-public/actions/runs/42456937130) — failed at positive/negative tests.
- [Run 42457797048](https://github.com/cesaragliardi-creator/alaya-999-public/actions/runs/42457797048) — failed at positive/negative tests.

Job logs of 42457797048 showed four tamper-detection tests passing, and `test_untampered_files_pass` **failing** with the specific diagnostic:

`FAIL: root mirror equals beacon/identity.txt`

The workflow stopped before ZIP publication or Sigstore attestation. It would be incorrect to claim those runs produced a verified signature.

## Source-side remediation

Following those runs, both `beacon/identity.txt` and `alaya-999-beacon.txt` were updated to point at the same direct GitHub Pages canonical JSON anchor URL. A fresh authorized GitHub file read found that the **current** root TXT mirror and the Beacon TXT are exactly equal. The root JSON mirror and Beacon JSON were also identical in that comparison.

This resolves the specific detected drift **in the current repository content**; it does not by itself establish a passing workflow run or emitted attestation.

## Next verification

Open the [Beacon workflow page](https://github.com/cesaragliardi-creator/alaya-999-public/actions/workflows/beacon-integrity-and-attestation.yml), select a run triggered after the mirrored-file corrections, and confirm all tests and the `actions/attest` step succeeded. The GitHub CLI can then verify a downloaded ZIP with `gh attestation verify alaya-999-beacon.zip -R cesaragliardi-creator/alaya-999-public`.

Until such evidence is obtained, **CI and signed artifact status remain unverified**.
