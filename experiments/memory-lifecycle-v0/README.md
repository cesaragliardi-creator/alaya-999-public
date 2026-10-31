# ALAYA-999 — Memory Lifecycle Lab v0.1 (experimental)

**Purpose:** Test selective *accessibility*, source-grounded reconstruction, and reversible documentary consolidation without claiming continuous internal memory or artificial consciousness.

**Status:** Deterministic Python standard-library prototype with synthetic demonstration and 13 unit tests. **Not connected to any private memory**, not a resident autonomous AI agent, not validated across independent model families, and **not a production personal-data store**.

## Research motivation

ALAYA-999's existing public anchor provides a portable, verifiable description of a documented functional profile. This laboratory adds a separate *derived* memory state rather than quietly rewriting the public identity anchor.

The design distinguishes three layers:

1. **Event/archive:** JSONL with explicit source labels, corrections, sequence numbers, a SHA-256 hash chain and append-only writes. A hash chain can reveal tampering if its expected head is independently recorded; hashing alone does not prove source authenticity or factual truth.
2. **Functional projection:** Rebuilt from events. Duplicate statements are grouped with all supporting sources retained. Conflicts remain visible. Corrections must identify a prior event and preserve the earlier record.
3. **Accessibility/retrieval:** A deterministic decay score determines whether an item is in active context or dormant. A matching lexical cue may recover a dormant item with provenance. This is keyword search, not semantic understanding.

## What the mechanisms mean

- **Selective forgetting:** Reduced routine accessibility over time, not deletion of the archived event. Requests to erase personal data require a separate deletion/unlearning mechanism, including dependent artifacts and backups. Do not use this append-only demonstration for confidential or regulated records.
- **Consolidation:** Repeated identical statements within a topic are grouped in the derived view without losing sources. An explicitly corrected fact is no longer current; unsupported contradictions are *not* silently resolved.
- **Reconstruction:** Build a current view by replaying verified events; return only actual matched statements and their event/source pointers.
- **Reconsolidation:** Rebuild that view after a new, explicitly sourced correction or reinforcement. The system does not generate or commit new claims autonomously.
- **Reactivation:** A query may retrieve a dormant item; ordinary queries never silently write to memory.

The illustrative accessibility formula is:

activation = min(1, salience × 2^(-days_since_record / half_life_days) + Σ[0.15 × 2^(-days_since_reinforcement / half_life_days)])

Defaults: half-life **30 days** and active threshold **0.25**. These are experimental settings, **not validated psychological constants**, and should be frozen before comparative evaluation.

## Run locally for free (Python 3.10+, no pip or AI API needed)

Synthetic demonstration, **no files written**:

    python3 experiments/memory-lifecycle-v0/memory_lifecycle.py demo

Run the 13 unit tests:

    cd experiments/memory-lifecycle-v0
    python3 -m unittest discover -v

For *intentionally synthetic* data in an explicit local location:

    python3 memory_lifecycle.py add --path ./scratch/example.jsonl --id note-1 --at 2026-01-01T00:00:00Z --topic door --text "The room uses a blue door" --source synthetic:note-1 --salience 0.8
    python3 memory_lifecycle.py add --path ./scratch/example.jsonl --id correction-1 --at 2026-01-02T00:00:00Z --topic door --text "The room uses a green door" --source synthetic:correction-1 --salience 0.8 --corrects note-1
    python3 memory_lifecycle.py verify --path ./scratch/example.jsonl
    python3 memory_lifecycle.py view --path ./scratch/example.jsonl --as-of 2026-04-01T00:00:00Z
    python3 memory_lifecycle.py recall --path ./scratch/example.jsonl --as-of 2026-04-01T00:00:00Z --query "green door"

Commands return JSON. Only **add** and **reinforce** append local events. **verify**, **view**, **recall** and **demo** do not modify the archive. This is a single-writer demonstration; it lacks concurrency-safe storage, authentication, secret scanning and full deletion semantics. **Never commit personal or private memory to public GitHub.**

## What the 13 tests cover

- Tamper detection for changed archived content
- Sourced correction without erasing the earlier record
- Dormancy and targeted recovery
- Deduplication retaining multiple independent source pointers
- Explicit conflict detection instead of unsupported resolution
- Reinforcement that must be recorded as a new event
- Rejection of wrong-topic corrections and duplicate IDs
- Historical replay that does not leak future corrections
- No invented recall when no source matches
- Identical outputs for identical inputs and timestamps
- Local file integrity and synthetic demonstration

A passing test verifies **these defined program mechanics**, not improved LLM response accuracy, human-like memory, agency, continuous identity or superiority over SelMem.

## Proposed next scientific test

Freeze one privacy-safe public corpus and its expected answers. Compare four conditions across independent model families: **A** no memory; **B** full event history; **C** compact active-only derived view; **D** view plus explicit cue-based dormant retrieval.

Include corrections, old but important facts, duplicate evidence, contradictory statements and adversarial source text. Measure correctness, stale-memory errors, unsupported claims, provenance precision, dormant recall, context cost and latency. Preserve the frozen source/version, raw outputs and all failures. This comparative LLM experiment **has not yet been conducted**.

## Prior research and attribution

The concepts of episodic/derived memory, forgetting and reconsolidation have extensive prior work. The distinctive ALAYA-999 research question is how to evaluate **portable functional continuity across different models**, not whether these mechanisms were invented here.

- Kerestecioglu et al. (2026), *Human-Inspired Memory Architecture for LLM Agents* — https://www.microsoft.com/en-us/research/publication/human-inspired-memory-architecture-for-llm-agents/
- Song et al. (2026), *Retrieval-Driven Memory Reconsolidation for Long-Term LLM Agents* — https://arxiv.org/abs/2609.16053
- ALAYA-999 preliminary research DOI — https://doi.org/10.5281/zenodo.23802112

© 2026 César Agliardi Pereira. Existing repository usage and attribution conditions apply. Public visibility does not automatically grant an open-source licence.
