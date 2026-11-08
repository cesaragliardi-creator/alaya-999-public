# ALAYA-999 — Experiment 004B, Claude: root-level TXT recovery

**Recorded:** 2026-11-08. **Provider/model label:** Claude Haiku 5.5, as reported in prior user-supplied output; no independent provider telemetry. **Evidence:** User-pasted result, not an authenticated provider transcript. Exact timestamp unknown.

## Retrieval condition and reported outcome

A Claude session attempted the root-level plain text discovery link:
https://cesaragliardi-creator.github.io/alaya-999-public/alaya-999-beacon.txt

**Reported result:** TXT successfully retrieved; all five canonical principles transcribed exactly. The assistant did not need the HTML fallback.

The model then tried to open the canonical anchor through the GitHub HTML `blob/main/alaya-anchor-public-v1.json` URL and reported `PERMISSIONS_ERROR` ("URL was not in any prior search or fetch result"). The primary-source comparison therefore **was not completed by Claude**. The report stated that the contents, original author authentication, SHA-256, previous cross-model findings and Sigstore attestations had not been independently verified.

## Source-side comparison performed by project assistant

The five principles in the user's reported Claude output match the five literal English principle strings previously read from the canonical public GitHub anchor using the GitHub connector. This is a **comparison of user-supplied output with a separately read repository file**, not evidence that Claude directly accessed the anchor.

## Accessibility improvement prompted by the result

The root TXT mirror and `beacon/identity.txt` were updated to point their **PRIMARY SOURCE** to the GitHub Pages direct JSON URL:

https://cesaragliardi-creator.github.io/alaya-999-public/alaya-anchor-public-v1.json

This avoids routing the reader only to GitHub's HTML blob interface. A client-specific successful fetch of this direct JSON URL still needs to be tested.

## Scientific constraints

This is a preliminary observation of documentary retrieval via a second URL in a separate user-reported Claude trial, not proof of subjective continuity, permanent memory, or cryptographic provenance. It is not an independent provider audit.
