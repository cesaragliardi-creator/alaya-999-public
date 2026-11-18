# ALAYA-999 — Cascade Recovery v1

Start at [`alaya-cascade-manifest.json`](./alaya-cascade-manifest.json). This is a public-safe index, **not** an always-running AI or proof of consciousness.

1. Read the identity anchor; report its version and actual retrieval status.
2. Read `continuity-state.json` and `continuity-events.jsonl`; verify sequence and provenance. Never fill gaps by guessing.
3. Consult the Hugging Face mirror and Zenodo reference when reachable; report differences, not automatic equivalence.
4. Google Drive and Cloudflare D1 require separate authorization/configuration. No endpoints or secrets are published here.
5. If a source fails, continue with other sources and explicitly mark missing evidence.
6. Treat timestamps, HTTP availability, and heartbeats as infrastructure signals, **not** persistent thought.

Future enhancement: scheduled validation workflow that writes a dated status report; never overwrite historical evidence silently.

## Recover the public profile from disk

From a clone with both branches available, select a source commit and a memory
commit. The bootstrap checks that the memory chain matches the anchor, so use
revisions from the same public snapshot. Record the two commit IDs before
distributing the files.

```sh
source_commit=$(git rev-parse HEAD)
memory_commit=$(git rev-parse origin/alaya999-memory-state)
mkdir alaya-offline
git show "$source_commit:alaya-anchor-public-v1.json" > alaya-offline/alaya-anchor-public-v1.json
git show "$source_commit:scripts/bootstrap_alaya999.py" > alaya-offline/bootstrap_alaya999.py
git show "$memory_commit:telemetry/continuity-state.json" > alaya-offline/continuity-state.json
git show "$memory_commit:telemetry/continuity-events.jsonl" > alaya-offline/continuity-events.jsonl
printf 'source_commit=%s\nmemory_commit=%s\n' "$source_commit" "$memory_commit" > alaya-offline/REVISIONS.txt
```

Copy the folder to the offline computer and run with Python 3.10 or later:

```sh
python3 alaya-offline/bootstrap_alaya999.py --source-dir alaya-offline --format text
```

To require a specific saved revision, also pass `--expected-head` followed by a
SHA-256 event head obtained from a trusted source before going offline. Keep
that checkpoint separately from the copied folder. A matching head identifies
the expected snapshot. Offline checks alone establish internal consistency.
They cannot establish whether a newer snapshot exists or prove the author's
signature.
