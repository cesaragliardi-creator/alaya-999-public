# ALAYA-999 Experiment 007 — Recover, Apply, Correct (preregistered pilot)

Date: 2026-11-08. Research design informed by public methodological comments from Hugging Face participants `nootxlm` and `SheilaMayoAI` on https://discuss.huggingface.co/t/independent-research-challenge-can-ai-memory-survive-across-different-models-alaya-999/191251 .

**Goal:** Determine whether new, isolated model sessions can (1) retrieve a recently published, entirely synthetic identity with no prior notoriety, (2) use previously documented commitments in a novel scenario, and (3) retain a dated correction without silently overwriting earlier claims.

This is a protocol **prepared**, not a study already run. Any later results must include raw prompt, response, timestamps, tool access and provider-disclosed model metadata.

## Experimental sources

- [Control identity A](identity-a.json) and [Control identity B](identity-b.json): two explicitly fictional, matched research-agent profiles with opposite but harmless procedural commitments.
- [Correction timeline](correction-events.jsonl): an initial plausible assertion and later evidence-backed correction; the model must prefer the corrected statement while recognizing the former.
- [Protocol and scoring](PROTOCOL.md): standardized procedure, control arms, objective measures and interpretation limits.

## Design precautions

- Use the exact same instructions and access conditions for each provider. New conversation, no personalization or previous project history; record if not demonstrably fresh.
- Do **not** put the answer text into the prompt. Supply only one assigned source URL or withhold a URL for control.
- Run an **anchor group**, a **no-anchor group**, and a **plain-facts document group**, with comparable token budgets.
- The profiles are synthetic and unrelated to any private people; the model must not claim subjective consciousness.
- The source documents and scoring rules are public before testing; this is a preregistered pilot, **not a hidden evaluator or a secure blinded benchmark**. Independent reviewers should create private unseen variations to rule out contamination.
- Do not claim a cryptographic signature, CI pass, or scientific validation without separate evidence.
