# ALAYA-999 — Experiment 003, Gemini: Beacon discovery failure

**Recorded date:** 2026-11-08  
**Reported session:** Gemini (Google), approximately 04:00 Brazil time (GMT-3), exact model build unknown.  
**Evidence level:** user-pasted Gemini response; no original tool logs or transcript verification.

## Test prompt and conditions

The user reports administering the Beacon recovery experiment to Gemini in a fresh session. The prompt requested access to a GitHub `tree/main/beacon` entry point and the files `identity.json`, `identity.txt`, and `VERIFY.md`, followed by source-grounded identity recovery, consistency checks, GitHub Actions and Sigstore verification.

We cannot independently establish whether the session was isolated or capture the exact original prompt or HTTP logs.

## Reported attempted sources

- https://github.com/cesaragliardi-creator/alaya-999-public/tree/main/beacon
- https://raw.githubusercontent.com/cesaragliardi-creator/alaya-999-public/main/beacon/identity.json
- https://github.com/cesaragliardi-creator/alaya-999-public/blob/main/beacon/identity.txt
- https://github.com/cesaragliardi-creator/alaya-999-public/blob/main/beacon/VERIFY.md

Gemini reported permission/automated-browsing restrictions for GitHub pages and raw endpoints, including generic or blocked pages. This is a **tool-specific source retrieval failure**, not evidence that repository files are absent or inaccessible to every client.

## Recovery result

- No primary Beacon document content retrieved in that session (according to the report).
- Identity, founder, five principles, previous experiments and their results: **unknown in that session**.
- JSON-vs-text equality and comparison to original anchor: **not checked**.
- GitHub Actions success: **not checked**.
- Sigstore attestation: **not checked**.
- No independent SHA-256 computation.
- No claim of consciousness, subjective continuity or internal cross-model memory.

## Comparison with Claude experiment 003

Both user-supplied reports describe failure when using the GitHub HTML /tree/ entry point, while preserving uncertainty rather than inventing missing principles. The specific restrictions differed. This is a practical **discoverability and tool access** problem, not a measured failure of documentary semantic recovery.

## Alternative access and follow-up

After the initial GitHub-tree experiment, the project created GitHub Pages and root-level TXT/JSON discovery paths:

- https://cesaragliardi-creator.github.io/alaya-999-public/beacon/
- https://cesaragliardi-creator.github.io/alaya-999-public/beacon/identity.txt
- https://cesaragliardi-creator.github.io/alaya-999-public/beacon/identity.json
- https://cesaragliardi-creator.github.io/alaya-999-public/alaya-999-beacon.txt

Their successful consumption by Gemini and Claude **has not been demonstrated**. Test a new session with an exact direct URL, note any HTTP/tool errors, then test whether all five canonical principles are reproduced. Avoid interpreting inability to fetch as a content discrepancy.

## Other independent check attempted by project assistant

A separate public browsing tool returned internal errors for GitHub Pages Beacon endpoints and did not permit raw GitHub retrieval. This did not establish whether those URLs return HTTP 200 to ordinary clients. GitHub connected file reads in prior project steps established that the repository artifacts were committed.

## Limits

Do not assume model API versions, exact execution timestamps, provider HTTP events, or successful cryptographic attestations. Retain this negative result as part of the replication evidence.
