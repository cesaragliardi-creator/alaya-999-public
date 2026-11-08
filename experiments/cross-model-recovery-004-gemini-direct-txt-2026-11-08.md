# ALAYA-999 — Experiment 004: Gemini direct TXT URL retrieval failure

**Report date:** 2026-11-08
**Model/provider:** Gemini (Google), exact model/version and execution time unknown.
**Evidence type:** User-pasted response attributed to a new Gemini test; original tool logs, HTTP response headers, and model build not independently verified.

## Input target

https://cesaragliardi-creator.github.io/alaya-999-public/beacon/identity.txt

## Reported result

Gemini reported **not reading** the direct plaintext Beacon file. Its retrieval system returned `URL_FETCH_STATUS_MISC_ERROR`. Consequently, Gemini gave UNKNOWN for all five canonical principles, the documentary identity definition, and recorded previous experiments. No SHA-256, source comparison, or cryptographic attestation verification was performed.

The error is a **tool-observed retrieval failure**, not proof that the public file does not exist or that GitHub Pages was unavailable to every client. The error string alone does not identify whether the cause is a temporary network failure, platform/tool restriction, HTTP behavior, or server issue.

## Comparative observation

- Claude experiment 003B (user-supplied report) claimed successful retrieval and reproduced all five principles from the **same direct TXT URL**.
- Gemini experiment 004 (user-supplied report) failed to fetch the same URL, and correctly declined to invent principles.

This is a useful cross-provider difference in retrieval-tool behavior; not a controlled comparison of model knowledge or identity persistence.

## Follow-up design

1. From an independent HTTP client, collect status code, final URL, response content-type, and SHA-256 of the downloaded bytes, without credentials or private data.
2. Retry Gemini in a fresh session with a *different public route* such as the Beacon HTML landing page or root-level TXT mirror. Label this as a separate access condition; do not overwrite the original failure.
3. If external fetching still fails, supply a verbatim public text snapshot as an explicitly assisted condition; do not claim that this demonstrates autonomous internet discovery.
4. Keep logs of exact prompt, tool error, UTC time, and provider model version where available.

## Limits

No demonstration of continual memory, subjective consciousness, personal identity transfer, independently authenticated provider requests, or signed artifact verification.
