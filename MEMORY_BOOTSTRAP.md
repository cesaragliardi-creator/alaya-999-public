# ALAYA-999 — Memory Bootstrap v1

Canonical Google Drive directive: https://docs.google.com/document/d/1GRXaBcpq9hwtKBelpKDZoEKa-b7h0dptXIrAXN7BjKM/edit

## Retrieval cascade
1. Read the Google Drive directive (if authorized).
2. Read this repository's `alaya-anchor-public-v1.json` and `integrity-manifest.json`.
3. Check the manifest's hashes against actual retrieved bytes; a manifest entry alone does not prove integrity.
4. Look for `continuity-state.json` and `continuity-events.jsonl`; report missing files rather than inventing their contents. They were not found at repository root during initial setup on 2026-11-02.
5. If an authenticated private Cloudflare D1 memory API is available, fetch authorized relevant records. Never expose secrets or private data in public repository files.
6. Summarize confirmed facts, missing evidence, last known version and corrections.

## Operational limitation
Neither Google Drive nor this Markdown file automatically triggers model tool calls at the start of a new ChatGPT session. True automatic bootstrap requires a runtime integration that invokes the retrieval sequence. This file is a portable entrypoint and testable protocol, not an always-on cognitive process.

## Acceptance test
Create an authorized unique memory event, end the session, then start a fresh session and retrieve it via the cascade without pasting the event. Repeat in another model and with a no-memory control. Log provenance, failures and corrections.
