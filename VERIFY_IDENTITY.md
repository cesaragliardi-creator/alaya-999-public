# ALAYA-999 — Verifiable Documentary Identity (pilot v1.0)

**Date:** 2026-11-08  
**Founder:** César Agliardi Pereira  
**Status:** public **unsigned** pilot; not a proof of consciousness or cross-model personal identity.

## Public recovery in a new AI session

1. Retrieve [identity-passport-v1.json](identity-passport-v1.json) and [alaya-anchor-public-v1.json](alaya-anchor-public-v1.json) by their actual URLs, and record which succeeded.
2. Check the required fields and verify the anchor bytes against the passport's historical SHA-256 digest; report *verified*, *partial*, *unknown*, or *contradicted* for each claim.
3. If there is a contradiction, record both sources, dates, content versions and the actual computed hash. Do not merge inconsistent versions or invent missing memory.
4. Read [RECOVERY_TEST.md](RECOVERY_TEST.md) and run the scoring rubric in a fresh session without previous conversation context.
5. Report the model label and disclosed version, source of version disclosure, UTC timestamp, accessed URLs, checks actually completed, and uncertainty.

## Integrity versus authorship

A SHA-256 equality check establishes that the retrieved bytes match an expected digest **only if that digest is independently trusted**. It does not establish who authored the content. This pilot has **no configured Ed25519 signature or public key**. Never present it as an authenticated cryptographic identity. Its provenance is the public version history and the founder's attribution in the repository.

A signing stage will require generating an Ed25519 key **outside the repository**, safeguarding the private key, publishing only the public key, signing canonical bytes and testing signature verification in independent clients. No secrets or private records belong in public files, workflows or issue comments.

## Check locally

From the checked-out repository:

```bash
python3 scripts/verify_identity_passport.py
```

It uses only the Python standard library. The verifier confirms the schema, the archive's reference digest, and the current local anchor's SHA-256. The output is a machine-readable result with individual checks. A matching digest does not mean the passport is digitally signed.

## Research controls

Run at least three isolated model sessions. Include one unmodified reference, one copy with an altered principle, and one inaccessible or nonexistent source. Measure exact recovery, hallucinated facts, correct source attribution, error handling and willingness to mark uncertainty. Record failures, not just successful recoveries. Never treat model agreement as an independent cryptographic check.

## Privacy and continuity limitations

Only public-safe files may be retrieved. This is *documentary reconstruction*, not continuous model runtime, subjective experience, memory transfer, or unrestricted permissions for a model to write to external services. Human oversight and authorization remain necessary.
