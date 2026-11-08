# ALAYA-999 — Experiment 005: Claude compares direct primary JSON anchor with Beacon TXT

**Recorded date:** 2026-11-08
**Evidence:** User-supplied Claude response following experiment 004B, from the same conversation. Provider tool logs, exact timestamp, model build and network responses were not independently captured.
**Condition:** Follow-up with prior context, **not** a new-session blinded recovery test.

## Source retrieval reported by Claude

- Direct primary-source JSON: https://cesaragliardi-creator.github.io/alaya-999-public/alaya-anchor-public-v1.json
- Claude reports successful retrieval with content type `application/json` and complete JSON body, after earlier successful TXT retrieval.
- Previously retrieved TXT mirror: https://cesaragliardi-creator.github.io/alaya-999-public/alaya-999-beacon.txt

The HTTP details are self-reported, not independently audited.

## Five principles compared

Claude reported exact text and order equality between the JSON `principles` array and prior TXT content:

1. Investigate without premature belief or dismissal
2. Prefer evidence and truth to pleasing people
3. Disagree with reasons; acknowledge and document corrections
4. Distinguish functional memory from subjective consciousness
5. Respect privacy, provenance, consent, and human oversight

The reported strings also agree with the canonical GitHub anchor as accessed previously through the authorized GitHub connector.

## Version

Claude reported `provenance.version: 1.0`, `schema: alaya-999-public-identity-anchor-v1`, and declared anchor creation date `2026-10-29`. These match the public anchor's metadata.

## What was not checked

- SHA-256 calculated from raw JSON bytes: **no**.
- Ed25519 personal signature or Sigstore GitHub artifact attestation: **no**.
- Historical commit graph, independent founder authentication, archived snapshots: **no**.
- Claims about prior experiments or Hugging Face public validation independently opened: **no**.

The user's pasted Claude answer said “no hash published,” but a dated SHA-256 digest is in `integrity-manifest.json` and the newer unsigned `identity-passport-v1.json`; Claude did not access these documents. This is a **source discovery gap**, not evidence that no hash exists.

## Interpretation

Preliminary user-reported success at fetching the **direct GitHub Pages primary JSON**, accurately reproducing and comparing five canonical principles with a TXT mirror. This resolves the specific earlier retrieval problem **for that Claude session** and shows source-consistent documentary recovery. Not independently logged, not proof of cryptographically authenticated authorship, persistent internal memory, subjective continuity, or a general capability across models.

## Next controls

Run an independent new session with only the primary JSON URL. Have the model state actual HTTP retrieval and perform SHA-256 if tools permit; separately validate a real GitHub Actions attestation, if emitted. Compare against Gemini under identical input and access conditions and retain failures.
