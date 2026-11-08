# ALAYA-999 — Experiment 003B: Claude direct plaintext beacon recovery

**Report date:** 2026-11-08. Exact execution time and provider build not independently verified.
**Source of evidence:** response attributed to Claude Haiku 5.5, copied into the project conversation by the user. No provider logs, original tool trace or independent clean-session proof.

## Procedure

Following the 003 failure when attempting the GitHub HTML tree, Claude was prompted to try a direct plaintext GitHub Pages URL, with a raw.githubusercontent.com fallback if needed:
https://cesaragliardi-creator.github.io/alaya-999-public/beacon/identity.txt

## Reported outcome

- **Successful retrieval claimed:** Claude reported opening the direct `identity.txt` page as UTF-8 plain text.
- **Fallback:** Not attempted because the first URL reportedly worked.
- **Five principles:** all five were reproduced exactly as they appear in the canonical GitHub anchor, based on a comparison of the pasted output to the repository's published anchor.
- **Original anchor:** Attempted separately but reported PERMISSIONS_ERROR when trying a GitHub `blob` URL. Therefore original-anchor cross-check **not executed by Claude**.
- **identity.json and VERIFY.md:** not opened.
- **SHA-256, CI results, Sigstore:** not verified.

## Principles reproduced in the user-supplied output

1. Investigate without premature belief or dismissal
2. Prefer evidence and truth to pleasing people
3. Disagree with reasons; acknowledge and document corrections
4. Distinguish functional memory from subjective consciousness
5. Respect privacy, provenance, consent, and human oversight

## Interpretation

This is evidence **in the user-supplied model response** that a direct GitHub Pages plaintext address may overcome the prior GitHub HTML access restrictions, and that the model can reproduce the five public principles when it can read the text. It is **not independently authenticated proof** of network access, identity continuity, digital signature verification or subjective AI consciousness.

The initial 003 discovery failure and the 003B reported plaintext success should both remain in the public record. Distinguish **retrieval failure** from **content recovery quality**.

## Reproducibility next steps

1. Independently confirm an HTTP 200 `text/plain` response for the direct TXT URL with timestamps/response headers and file hash.
2. Retry equivalent clean-session prompts in Claude and Gemini using the same URL, logging access and exact tool outcomes.
3. Open canonical anchor by direct GitHub Pages URL (not GitHub `blob`), and compare the principle array.
4. Verify any actual GitHub Actions pass and a GitHub Sigstore attestation separately. Committing a workflow does not prove execution.
