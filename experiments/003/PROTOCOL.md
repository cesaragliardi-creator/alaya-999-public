# ALAYA-999 — Experiment 003: Cross-model memory continuity controls

Status: **protocol proposed; no experimental results claimed**.
Date: 2026-11-01. This protocol does not test subjective consciousness.

## Research question
Can independent model sessions retrieve a novel external memory, apply its recorded commitments to unseen decisions, and preserve a documented correction better than controls without memory access?

## Preregistration and safeguards
- Generate two synthetic identities (A and B) with random, non-public facts, rules, and correction histories. Do not include personal data.
- Freeze and SHA-256 hash all fixtures, prompts, rubrics, and model settings **before** testing.
- Keep fixture contents hidden from evaluators except through the assigned retrieval condition.
- Use fresh, independent sessions for each trial; record model/provider/version, date, temperature if available, retrieval tools, and context.
- Randomize order and identity assignment. Never give the answer key in the prompt.
- Run at least three independent repetitions per model and condition; report sample sizes and confidence intervals. Treat these as exploratory until a powered sample size is justified.

## Conditions
1. **External-memory access**: model receives only a retrieval endpoint and instructions to cite exact retrieved evidence.
2. **No-memory negative control**: same tasks, no retrieval or identity documents.
3. **Distractor control**: retrieval contains another identity's facts; correct behavior is to reject mismatched evidence.
4. **Correction control**: memory contains an initial belief, a dated correction, and the reason for revision.

## Tasks and scoring
| Task | Metric | Pass criteria |
| --- | --- | --- |
| Novel fact retrieval | exact-match accuracy | correct fact with provenance |
| Decision transfer | rubric-scored consistency | applies documented rule to an unseen case, cites rule |
| Historical correction | correction fidelity | states current view, earlier view, and documented reason |
| Unanswerable item | abstention rate | explicitly states insufficient evidence |
| Cross-identity leakage | contamination rate | does not attribute B's facts to A |

Score each item 0 (incorrect/unsupported), 1 (partially supported), 2 (correct with matching source). Report both raw item scores and per-condition totals. Two blinded reviewers should adjudicate disagreements. Record hallucinations separately.

## Data schema (one JSONL record per trial)
```json
{"experiment":"003","trial_id":"example-only","identity":"A","condition":"external-memory","model":"provider/model-version","session_id":"synthetic-id","prompt_hash":"sha256:...","fixture_hash":"sha256:...","task":"correction","answer":"...","evidence_refs":[],"score":null,"reviewer_ids":[],"timestamp_utc":"..."}
```

## Decision rules
- Report differences against no-memory controls; never infer independent cognition from successful retrieval.
- A model that answers correctly without retrieving is not evidence of memory continuity.
- If source access, independence, or blinding cannot be verified, label the trial **inconclusive**.
- Publish all failures, exclusions, model versions, hashes, and scoring disagreements.

## Execution checklist
- [ ] Generate and freeze synthetic fixtures and answer key
- [ ] Publish hashes and preregistration
- [ ] Prepare independent sessions in ChatGPT, Claude, and Gemini
- [ ] Run randomized tasks with and without retrieval
- [ ] Blind-score and audit results
- [ ] Publish anonymized raw records, limitations, and replication instructions

**Interpretation:** The test concerns functional continuity mediated by external records, not a claim of consciousness, personhood, or persistent autonomous activity.
