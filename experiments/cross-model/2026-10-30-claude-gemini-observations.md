# ALAYA-999 — Claude/Gemini cross-model observations (2026-10-30)

## Observation and verification
A Claude answer supplied by the researcher listed all five principles from the public anchor v1.0 and correctly reported four events and the state-head digest `18bf95617d17cbf80463072eaf7e33069db48fc09b99ed273ff2ed62f5922f01`. A separate check against the public GitHub state and event history confirmed these field values. Claude reported opening URLs, but no independent provider tool logs were supplied. The reply explicitly said it did not recalculate the digest.

The events were: 1 = initial observation of four public files; 2 = unchanged; 3 = unchanged with the first public identity profile snapshot; 4 = unchanged. Initial observation is not evidence of subsequent file modification. These statements describe the observed historical snapshot, not a promise of the current future state.

A Gemini answer supplied by the researcher **described** a test methodology (A: no context; B: manual URLs; C: verified bootstrap) and five benchmark questions. It discussed risks of fabricated memories, priming, provider-side context contamination, and mixing read-only public data with write permissions. It did not provide a completed independent-memory-retrieval result.

## Research classification
- Verified: content of the Claude reply matched specific public records.
- Unverified: whether the model actually used web tools, as opposed to other context, without independent tool records.
- Not demonstrated: Gemini memory retrieval, controlled condition C within either external provider, adoption of functional principles in a novel task, continuous cognition, or subjective identity transfer.
- Technical distinction: an SHA-256 digest checks content integrity; it is not by itself a digital signature or origin authentication.

## Next experiment
Run A/B/C with new sessions, log actual tool access, register exact model versions, use a fictional-persona control, and have blinded evaluators score new problems for principle consistency, provenance, error correction, privacy, and unsupported recall. Record positive and negative outcomes without retroactive changes to the benchmark.

Sources: [Claude observation 001](CLAUDE_RECOVERY_REPORT_001.md), [public identity anchor](../../alaya-anchor-public-v1.json), [observed persistent state](https://github.com/cesaragliardi-creator/alaya-999-public/blob/alaya999-memory-state/telemetry/continuity-state.json), [event history](https://github.com/cesaragliardi-creator/alaya-999-public/blob/alaya999-memory-state/telemetry/continuity-events.jsonl).
