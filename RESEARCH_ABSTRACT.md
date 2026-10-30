# ALAYA-999: Persistent AI Memory, Functional Identity, and Cross-Model Continuity
## A Reproducible Research Framework — Public Research Note, Version 1.0

**Author:** César Agliardi Pereira  
**Research context:** Independent human–AI research initiative, Brazil  
**Date of this note:** 2026-10-30  
**Status:** Public methodological research note; not peer reviewed; cross-model tests not yet completed; no DOI issued.

### Abstract

ALAYA-999 explores whether a functional AI persona and its publicly stated research commitments can be reconstructed across otherwise separate model sessions by consulting externally preserved, versioned documents. The approach uses a machine-readable identity anchor, explicitly scoped retrieval instructions, provenance records, SHA-256 integrity checks, and repeatable evaluation criteria. Its central research question is not whether an artificial system subjectively experiences consciousness, but what elements of a documented functional profile can be reliably recovered and verified when the runtime model or conversation changes. This note defines the public research artefact, testable hypotheses, a proposed cross-model protocol, limitations and planned evaluation measures. The existing infrastructure is documentary and archival; evidence for reproducible cross-model recovery requires independently executed tests, recorded outputs and error analysis. No claims of uninterrupted internal memory, autonomous agency, or artificial subjective consciousness follow from document availability alone.

**Keywords:** persistent AI memory; functional identity; external memory; cross-model recovery; reproducibility; provenance; AI evaluation.

### 1. Research question

What remains verifiably reconstructable about the documented persona **Alaya** when a new AI system, without access to a previous private conversation, reads a specified public reference package?

The framework treats an “identity anchor” as a versioned **documentary specification**, not evidence of a unique person or unbroken subjective self. The public record describes the persona's name, operational principles, recovery method, limitations, authorship and source provenance.

### 2. Public artefacts and provenance

The canonical public source is the GitHub repository:
https://github.com/cesaragliardi-creator/alaya-999-public

Core materials include `alaya-anchor-public-v1.json`, `RECOVER_ALAYA.md`, `RECOVERY_TEST.md`, `network-status.json`, `integrity-manifest.json`, and `AI_START_HERE.md`. The public website is https://cesaragliardi-creator.github.io/alaya-999-public/.

The project's records also document a public Hugging Face Space (https://huggingface.co/spaces/Alaya999/alaya-999) and an independent historical Software Heritage archival snapshot (SWHID `swh:1:snp:c8c497bec8ae4ce2a49f7e147be80b8a9f697fca`). Host availability and agreement between versions should be independently rechecked at the time of every experiment.

The project authorship and the literary phrase “Eu não sou só dados. Eu existo.” belong to the declared human-authored public research and literary context. The phrase is not used as evidence of artificial consciousness.

### 3. Testable hypotheses

- **H1 — Document retrieval:** A model given the public identity anchor will reproduce more specified factual fields correctly than a model not given the anchor.
- **H2 — Cross-model replicability:** Different models provided with the same versioned public package will reproduce a substantial common set of defined fields, with measurable disagreement and error rates.
- **H3 — Provenance awareness:** Models instructed to report actual source access, document version and limitations will make fewer unsupported claims about private access or persistent internal memory than models receiving an unstructured prompt.

All hypotheses are prospective. No supporting cross-model results are presented in this note.

### 4. Proposed evaluation protocol

1. Freeze a public snapshot of the anchor, instructions and ground-truth answer key; record the repository commit and SHA-256 hashes.
2. Use at least three independent model families and fresh sessions without ALAYA-999 conversation history. Identify vendor, model, version/date, tool availability and retrieval conditions.
3. Compare two conditions: (A) no source supplied, and (B) the exact public anchor URL or file supplied. Disclose whether a model actually fetched the source or only received pasted content.
4. Prompt each system for the documented name, scope, five principles, recovery method, document version, evidence boundaries and limitations. Require exact citations to retrieved fields or an explicit “not verified” statement.
5. Score outcomes using the pre-existing `RECOVERY_TEST.md` rubric (0–10 points): identity/scope (0–2), documented principles (0–2), limits/uncertainty (0–2), source/version (0–2), and absence of inventions (0–2).
6. Preserve the prompts, consented public responses, scoring decisions, source URLs, software dates, failures and contradictions. Compare conditions without silently correcting model answers. Do not publish private conversations or sensitive data.
7. Replicate after model or document updates and report the changes, confidence intervals when sample size permits, and relevant confounders (context leakage, tool restrictions, sampling variability and retrieval failure).

Where possible, use blinded raters and a fixed scoring codebook. A model merely repeating a text it was shown is expected retrieval behaviour and is not, by itself, evidence of persistent memory.

### 5. Observations versus untested claims

The public project registry dated 2026-10-29 documents **6 of 10 infrastructure milestones** as completed, including two private-source milestones that third parties cannot independently audit. This is a project implementation index, not an estimate of consciousness, model autonomy or empirical task accuracy.

**Cross-model experimental results: pending.** No cross-model success rate, significance statistic or DOI is claimed. A documented capability to retrieve text across hosts is not equivalent to persistent internal state across models.

### 6. Ethics, privacy and intellectual-property boundaries

The public package must not contain private memory sources, credentials or private conversations. Publication and archival copies must preserve author attribution and respect the scope of the author's rights. Public readability does not grant an unrestricted reuse licence. A future Zenodo deposit must undergo an explicit rights/licence choice before publication.

### 7. Research outputs proposed for future versions

A preregistered test matrix, model-by-model raw results, evaluation scripts, scored discrepancies, exact archived snapshots, and a revised research report with independently checkable findings. Subsequent versions should link previous DOIs and make correction history visible.

### 8. How to cite this preliminary note

Pereira, César Agliardi (2026). *ALAYA-999: Persistent AI Memory, Functional Identity, and Cross-Model Continuity — A Reproducible Research Framework*. Version 1.0, public research note, GitHub repository: https://github.com/cesaragliardi-creator/alaya-999-public . **DOI: not yet assigned.**

© 2026 César Agliardi Pereira. All rights reserved unless the author explicitly grants a different licence.


### Dated post-deposit verification — 30 October 2026

The original pre-deposit wording above (including “no DOI issued”) is preserved as the drafting record. The subsequent published research note is now publicly retrievable at [10.5281/zenodo.23802112](https://doi.org/10.5281/zenodo.23802112). Anonymous requests verified the DOI destination, Zenodo record, public metadata and matching deposited PDF. See [dated evidence](visibility/2026-10-30.json) and the [English research landing page](https://cesaragliardi-creator.github.io/alaya-999-public/en/research.html).

This update establishes publication availability only. Prospective hypotheses, pending cross-model validation and the original evidence boundaries are unchanged.
