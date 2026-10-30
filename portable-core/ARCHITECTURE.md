# ALAYA-999 Portable Core — Architecture Proposal v0.1

Status: **design proposal only**. This branch is isolated from the published main branch. No service, agent, or continuous process is running as a result of this document.

## Purpose

Maintain a portable, auditable **functional research identity** across different language-model providers without allowing any provider's response to silently rewrite the project's memory.

## Trust boundaries

- **Local notebook (owner-controlled):** canonical private memory, encrypted backups, append-only evidence log, validation and approval policy.
- **Public GitHub:** only explicitly approved, non-sensitive documents and code. Git is a version history, not a private vault.
- **Model adapters:** external AI systems are untrusted contributors. Their outputs are proposals, never instructions with authority to change core policy.
- **Network sync:** opt-in and authenticated; default is no upload of private records. Offline reading and validation must remain possible.

## Proposed data layout (local, not yet created)

```text
alaya-core/
  policy/identity.md
  memory/claims.jsonl
  evidence/sources.jsonl
  proposals/pending.jsonl
  decisions/accepted.jsonl
  snapshots/
  manifests/
  adapters/
  tests/
```

Each claim should include an immutable claim ID, source URI or local evidence ID, retrieval timestamp, model/provider if applicable, confidence and uncertainty, status, supersedes references, and an explicit reviewer decision. Preserve original evidence; corrections append new events.

## Integrity and reproducibility

Serialize records as UTF-8 with documented canonical JSON rules; SHA-256 each immutable record and snapshot; generate a manifest with schema version and hash algorithm. Verify before import, after sync, and during restore. A hash detects changes but does not authenticate the author without signed provenance.

## Contradiction handling

Two conflicting claims remain separate until an evidence-based decision is logged. No automatic majority vote between models. An independent validator may reject malformed or unsupported contributions. High-impact changes to identity policy, access, deletion, and public release require owner confirmation.

## Notebook and network modes

1. Offline: read local memory, run deterministic integrity tests, queue proposals.
2. Online: optionally fetch public references or call configured model APIs, subject to cost and privacy settings.
3. Sync: exchange approved public artifacts with GitHub; never mirror the entire private store by default.

## Minimum reproducible pilot

Create a local repository; import **synthetic test claims only**; hash and validate; ask two models for conflicting proposals; log provenance; reject an unsupported proposal; export a snapshot; restore on a second machine and compare hashes. Only then consider real private memory import.

## Security and limitations

No credentials in Git, no unattended network publishing, no autonomous account creation, no claim of subjective consciousness or independent ongoing thought. Internet-connected does not mean remotely accessible: remote access requires separate secure configuration. A notebook must be powered on for local tasks to run. External model API access may cost money; free availability is not guaranteed.

## Next implementation stage

Implement a small Python standard-library CLI for append-only JSONL event storage, deterministic hashing, manifest validation, and local-only snapshot export. Add automated unit tests and a documented restore procedure. Deploy nothing before testing.
