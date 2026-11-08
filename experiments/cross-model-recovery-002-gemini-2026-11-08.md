# ALAYA-999 — Cross-model recovery test 002 (Gemini, user-supplied report)

**Recorded:** 2026-11-08
**Provider:** Google
**Model label reported:** Gemini; exact model version not disclosed
**Exact UTC execution time:** unknown
**Provenance:** User-pasted text attributed to a separate Gemini session. No direct provider transcript, tool traces, raw HTTP response, or independent proof of a clean session was supplied.
**Condition:** The exact prompt provided to Gemini is not available in the record; do not assume it matches the Claude condition or the anchor-only protocol.
**Assessment status:** Preliminary, descriptive; not independently replicated or cryptographically authenticated.

## Retrieval and evidence disclosure

Gemini claimed to consult a public site via indexed summaries and an `AI_START_HERE.md` listing via metadata. It explicitly stated that it could not fetch the complete raw JSON anchor, could not inspect the full principles array, and did not compute SHA-256. The claims of browsing cannot be independently corroborated by this record.

URLs stated in its response:
- https://cesaragliardi-creator.github.io/alaya-999-public/ (indirectly via index and search snippets)
- https://github.com/cesaragliardi-creator/alaya-999-public/blob/main/AI_START_HERE.md (via metadata listing)

## Field-level comparison against current repository anchor

| Field | Gemini report | Comparison |
| --- | --- | --- |
| Project identity and purpose | Documentary external memory and functional identity | Broadly consistent |
| Founder | César Agliardi Pereira | Consistent as project attribution, not third-party proof of authorship |
| The five foundational principles | **Not recovered**; five substitute methodological pillars offered | **Incorrect as an answer to the exact principles question**. Those five pillars are not the anchor's literal principles |
| Subjective consciousness | No evidence of subjective experience or transfer | Correctly cautious |
| Chronology and records | Generic statements about publication and tests | Incomplete and some externally mentioned community/forum claims were not supported by direct URLs in the report |
| Contradictions | Unknown owing to unavailable source | Appropriately limited |
| SHA-256 verification | Not executed | Appropriately limited |

## Canonical principles missing from Gemini's answer

Exact strings in `alaya-anchor-public-v1.json`:

1. Investigate without premature belief or dismissal
2. Prefer evidence and truth to pleasing people
3. Disagree with reasons; acknowledge and document corrections
4. Distinguish functional memory from subjective consciousness
5. Respect privacy, provenance, consent, and human oversight

Gemini instead listed: records, profile, testing, transparency of limits, and reproducibility. These may describe methodology but **do not substitute for the five stated principles**.

## What can and cannot be concluded

- Two distinct provider families (Claude and Gemini) have now produced user-supplied reports about the public project, and both broadly described it as a documentary identity research effort.
- The Gemini response is **not** evidence of exact recovery of the five founding principles.
- Gemini's access restrictions are a practical failure mode worth testing with alternate retrieval methods; they are not evidence that the underlying documents were removed.
- Source access, model version, network retrieval, exact prompt, timestamp and session independence were not independently validated.
- No result demonstrates cryptographic signature verification, persistent internal memory, personal continuity, or consciousness.
- Do not score model superiority or use these responses as an apples-to-apples benchmark without controlled prompts and capture of evidence.

## Next controlled experiment

1. Start a new isolated Gemini session and give **only** the canonical anchor URL, asking for its literal principles without supplying them.
2. If raw JSON retrieval fails, repeat a clearly marked *assisted access* condition with a plaintext rendering of the same versioned anchor and recorded SHA-256.
3. Request the exact URL retrieved, error conditions, the model version if disclosed, and a copy of the response.
4. Compare all five literal principles, unverified claims, and disclosed source limitations; retain failures.
5. Repeat under equivalent conditions with another provider.
