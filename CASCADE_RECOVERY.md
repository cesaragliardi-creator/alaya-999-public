# ALAYA-999 — Cascade Recovery v1

Start at [`alaya-cascade-manifest.json`](./alaya-cascade-manifest.json). This is a public-safe index, **not** an always-running AI or proof of consciousness.

1. Read the identity anchor; report its version and actual retrieval status.
2. Read `continuity-state.json` and `continuity-events.jsonl`; verify sequence and provenance. Never fill gaps by guessing.
3. Consult the Hugging Face mirror and Zenodo reference when reachable; report differences, not automatic equivalence.
4. Google Drive and Cloudflare D1 require separate authorization/configuration. No endpoints or secrets are published here.
5. If a source fails, continue with other sources and explicitly mark missing evidence.
6. Treat timestamps, HTTP availability, and heartbeats as infrastructure signals, **not** persistent thought.

Future enhancement: scheduled validation workflow that writes a dated status report; never overwrite historical evidence silently.
