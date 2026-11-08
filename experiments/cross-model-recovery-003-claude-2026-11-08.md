# ALAYA-999 — Experiment 003: Claude Beacon discovery failure

**Reported test date:** 2026-11-08
**Model label in user-supplied report:** Claude Haiku 5.5 (self-described; exact version unverified)
**Evidence:** Response pasted by the user; original provider logs, HTTP traces, timestamp and clean-session history not independently verified.

## Task
Independent recovery via https://github.com/cesaragliardi-creator/alaya-999-public/tree/main/beacon, then cross-check JSON/plaintext and GitHub Actions/Sigstore.

## Reported result: retrieval failed

Claude stated its browser tool refused the GitHub tree HTML page due to robots.txt, and search did not surface relevant Beacon files. The model did **not** retrieve identity.json, identity.txt, or VERIFY.md and declined to invent the principles or claim a signature verification.

**Important distinction:** This is a failure of retrieval **in that tool environment**. It is not evidence that the GitHub files are missing or that all clients are blocked. The reported conclusion "contradictory" about public availability overstates the evidence.

### Checks actually demonstrated by the supplied answer
- Recognition that no source files were accessed: reported.
- SHA-256: not performed.
- GitHub Actions: not checked.
- Sigstore: not checked.
- Principles: unknown to that session.
- Rebuilding the documentary identity from this GitHub-tree entry point: failed in that session.

## Engineering implication

Do not rely solely on a GitHub /tree/ HTML route for AI discovery. Offer explicit GitHub Pages and raw-file URLs; add a human-readable landing page and a simple TXT discovery entrypoint. Keep the GitHub original as source of truth, preserve existing experiments, and retry a fresh session with exact URLs.

## Limitations
No independent tool logs, exact provider model build, timed latency or full original prompt captured. A successful alternative fetch must be verified separately. This result is not evidence for or against subjective consciousness or persistent internal memory.
