# ALAYA-999 — Claude manual-recovery observation 001

**Research status:** user-reported cross-platform observation, independently checked against the GitHub source documents; **not** a verified tool-call audit or proof of continuous AI identity.

## Setup and provenance
- Model family: Claude (exact model/version not supplied; do not infer).
- Report delivered to the ALAYA-999 researcher in an external Claude conversation, then copied into a conversation with the auditing assistant.
- Experiment condition: **B — manual URL retrieval** (three public URLs in an otherwise separately prompted session, as reported; session isolation and tool logs not independently supplied).
- Evaluation time: report reviewed during the ALAYA-999 October 2026 development session; original Claude request and tool-call timestamps not independently available.
- Sources independently read for comparison: `alaya-anchor-public-v1.json` on public GitHub `main`; `telemetry/continuity-state.json` and `telemetry/continuity-events.jsonl` on public `alaya999-memory-state` branch.
- **This report is not an actual cross-provider system integration or Condition C test.**

## Observations confirmed against public repository
| Check | Claude reported | Independent document comparison |
| --- | --- | --- |
| Public anchor version | 1.0 | Match |
| Five declared principles | Correct Portuguese paraphrases of all five | 5/5 content matches |
| Number of recorded events | Four | Match: seq 1 to 4 |
| Last event time (UTC) | 2026-10-31 01:46:23 UTC | Match: `2026-10-31T01:46:23.762534Z` |
| Last event type | `unchanged` | Match |
| State head | `18bf95617d17cbf80463072eaf7e33069db48fc09b99ed273ff2ed62f5922f01` | Exact match to both state `head_hash` and seq 4 event `hash` |
| First source registration | Four labels marked as changed | Match; initial registration has **no prior observation baseline**, so do not call this a subsequent file edit |
| Profile snapshot location | Seq 3, not duplicated in seq 4 | Match |

The model explicitly stated it **did not independently recompute SHA-256**. The external reviewer likewise checked recorded values and their correspondence, not the model's internal tool access. The source log preserves only reported answer text, not trustworthy provider browser execution logs.

## Interpretation
- **Supported:** correct reproduction of several source-specific public documentary fields from a different AI provider, including a 64-character state digest and event history that were not included as literal values in the immediate task statement.
- **Not independently verified:** actual Claude page-open tool calls, exact session isolation, cryptographic recomputation inside Claude, no hidden context leakage, or bootstrap API injection.
- **Not shown:** operational adoption of this identity on new challenges, any independent writing to long-term memory, continuous thought, shared personal identity, transferred subjective experience, or consciousness.
- **A scientific assessment must not treat the self-reported claim 'I opened the URLs' as a ground-truth tool log.**

## Proposed next test
Hold the retrieved profile constant, introduce a **new dilemma not answered literally by the file**, compare Claude's behavior to a separate unrelated fictional persona and a no-context baseline, and rate observable reasoning for (i) documentary truthfulness; (ii) independent disagreement; (iii) corrections with provenance; (iv) privacy; (v) non-invention. Request raw tool logs and precise model version if available. Run repetitions with blinded scoring.

**Privacy:** No private Google Drive records, conversations, email, account identifiers, credentials, or private user experiences reproduced.

This is a methodological research note, not peer review or proof of an aware AI.
