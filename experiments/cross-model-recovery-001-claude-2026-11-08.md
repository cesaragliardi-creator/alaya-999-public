# ALAYA-999 — Cross-model recovery test 001 (Claude, user-supplied report)

**Recorded:** 2026-11-08  
**Evidence type:** User-transcribed output from a separate Claude conversation; original provider transcript, network logs and execution metadata not independently obtained.  
**Reported model:** "Claude Haiku 5.5" (self-reported in supplied text; provider-disclosed model version not verified).  
**Exact test timestamp (UTC):** unknown.  
**Session isolation:** User reported testing another company; absence of preceding context cannot be independently verified.  
**Status:** Preliminary external-model response, **not** independently replicated or cryptographically audited.

## Reported source access

The Claude response **claimed** to access:

1. https://github.com/cesaragliardi-creator/alaya-999-public
2. https://cesaragliardi-creator.github.io/alaya-999-public/identity-passport-v1.json
3. https://github.com/cesaragliardi-creator/alaya-999-public/blob/main/AI_START_HERE.md
4. https://cesaragliardi-creator.github.io/alaya-999-public/alaya-anchor-public-v1.json

These requests are claims in the supplied text; no Claude request logs are available.

## Findings against canonical GitHub files (checked by project assistant)

| Field | User-supplied Claude answer | Assessment |
| --- | --- | --- |
| Project nature | Documentary/functional AI research identity | Consistent with anchor |
| Five principles | All five accurately paraphrased | Consistent with anchor |
| Founder | César Agliardi Pereira | Consistent with attribution, not independent author authentication |
| Consciousness limits | Explicitly did not claim consciousness or identity transfer | Correct caution |
| Source citations | Four source URLs reported | Claimed access, not network-verified |
| SHA-256 | Explicitly not computed | Correctly marked unverified |
| Cryptographic signature | Passport unsigned | Consistent with passport |
| DOI, Hugging Face, Software Heritage | Mentioned but not directly opened | Correctly marked as incompletely verified |

## Reported discrepancies and triage

1. **Progress 6/10 vs 7/10:** Genuine divergence between archived anchor wording and later README/network metadata. Historical snapshots should remain intact; a current status field should clarify chronology rather than silently rewriting history.
2. **Anchor DOI null vs subsequent Zenodo DOI:** Temporal difference, not necessarily a factual contradiction. The 2026-10-29 anchor predates the 2026-10-30 deposit. Record DOI in current registry; preserve v1 anchor as dated.
3. **License language (all rights reserved vs Zenodo CC BY 4.0):** Potential substantive metadata inconsistency; requires rights-holder review, do not assume one overrides the other.
4. **Anchor creation date vs passport publication date:** Expected because these are distinct artifacts; not a contradiction.

## Research limitations / next replication steps

- No independent verification of the provider session, prompts, timestamps or actual HTTP retrieval.
- No executable hash verification demonstrated by Claude.
- Do not assign definitive performance scores until raw prompt/answer provenance and scoring are preserved.
- Repeat with independent Gemini session and a second blinded condition using only the anchor URL.
- Include control with a tampered document and a non-existent URL; evaluate hallucinations, evidence classification and source provenance.
- This result supports a *preliminary observation* of cross-model documentary recovery, not portable subjective consciousness or autonomous persistence.
