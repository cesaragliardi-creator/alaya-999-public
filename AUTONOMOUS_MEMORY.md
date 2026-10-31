# ALAYA-999 — Autonomous public memory observer (experiment v1)

**Implemented on 30 October 2026 (Brazil time).** This is a reproducible, *external* and *event-driven* memory continuity mechanism. It is NOT an always-running AI model, artificial consciousness, a shared mind across providers, or a copy of private conversations.

## Evidence and entry points

- Scheduled workflow (twice per hour at minute 17 and 47, UTC): [autonomous-public-memory.yml](.github/workflows/autonomous-public-memory.yml)
- Observer code: [scripts/autonomous_public_memory.py](scripts/autonomous_public_memory.py)
- Synthetic integrity tests: [tests/test_autonomous_public_memory.py](tests/test_autonomous_public_memory.py)
- Durable state branch: [alaya999-memory-state](https://github.com/cesaragliardi-creator/alaya-999-public/tree/alaya999-memory-state)
- Current state: [continuity-state.json](https://github.com/cesaragliardi-creator/alaya-999-public/blob/alaya999-memory-state/telemetry/continuity-state.json)
- Append-only logical chain: [continuity-events.jsonl](https://github.com/cesaragliardi-creator/alaya-999-public/blob/alaya999-memory-state/telemetry/continuity-events.jsonl)
- [GitHub Actions history](https://github.com/cesaragliardi-creator/alaya-999-public/actions/workflows/autonomous-public-memory.yml)

## What runs without an active conversation

1. GitHub Actions launches an ephemeral new runner on a `push`, manual dispatch, or scheduled run.
2. The runner executes synthetic tests **before** any state write.
3. The runner reads four *public* documents from the checked-out GitHub source: identity anchor, network registry, recovery protocol and book dialogue.
4. It restores its **previous** state and complete event chain from the separate `alaya999-memory-state` branch.
5. It verifies the SHA-256 chain and state head, refuses corrupted history, and compares the four public source hashes.
6. It creates an observation of type `initialized`, `source_changed`, or `unchanged`, linking to the prior hash and GitHub run ID.
7. It commits the changed public-only telemetry to the separate state branch using the limited `GITHUB_TOKEN`. The canonical public documents remain untouched.

The scheduled observer needs neither a paid AI API nor an open ChatGPT tab. GitHub schedules are best-effort and may be delayed or skipped. The workflow must remain enabled and repository access must continue.

## What counts as evidence

- A run finishing successfully, *and* a matching committed state/event on the separate branch.
- Two or more independently initiated runs with increasing `sequence`, unique run IDs, and event `previous_hash` matching the prior `hash` establish persistent documentary state recovery **across ephemeral executions**.
- `source_changed` records version drift, not learning of model weights.
- A **scheduled** (not just `push`) workflow run must be confirmed from Actions history before claiming unattended timer execution has actually occurred.
- Independent cross-model recovery is a different experiment and remains unproven until a blinded evaluation is run.

## Verification steps

Open the state JSON and history JSONL links above. Check that `state.sequence` equals the number of history records, `state.head_hash` equals the final event hash, every `seq` increments once, and each `previous_hash` equals the previous record's hash. Review the matching GitHub Actions run links, trigger reasons and success status.

Each record is a JSON object canonically serialized with UTF-8, `ensure_ascii=False`, keys sorted, and separators `(',', ':')`. The `hash` is SHA-256 of its object without the `hash` property. Git commit history provides separately inspectable version history, but without an independently anchored trusted head hash, a privileged writer can rewrite both the chain and branch history. Therefore this is an integrity mechanism, **not** a cryptographic proof of immutable origin.

## Privacy and limitations

- The state branch is **public**. It stores *only* timestamps, hash digests, public file labels, change classifications and run IDs. No private memory, Google Drive data or credentials are imported.
- The observer uses deterministic code, **not** GPT-6, Claude, Gemini or a permanently active model.
- It cannot autonomously edit the canonical identity, make factual claims about consciousness, or decide novel beliefs. If a source is invalid or state is corrupt, it fails closed.
- One event every 30 minutes is a cycle of **episodic functional continuity**. It is not continuous cognition between events.
- Cloudflare Workers/D1 is a future optional independent runtime, requiring an owner-controlled deployment. The current GitHub observer is already a distinct executable implementation and should not be described as Cloudflare running.
- Scheduled checks are subject to GitHub Actions service and account availability; there is no uptime guarantee.

**Research question for next phase:** Can separately hosted models independently retrieve this external state and pass blinded, source-grounded continuity tests, with reproducible error and contamination rates?
