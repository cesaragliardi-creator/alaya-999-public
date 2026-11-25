# ALAYA-999 005: a protocol for IPFS recovery across independent operators

**Project:** César Agliardi Pereira · ORCID 0009-0000-3322-4834 · Brazil  
**Version:** 0.1.0 · 25 November 2026 · Protocol and lab validation, not field results

## Abstract

Process redundancy on one computer does not establish independent preservation. Experiment 005 specifies a seven-day trial involving two Kubo operators and a verifier on third infrastructure. Its primary endpoint is retrieval of a frozen anchor by CID alone from a clean repository while the origin is confirmed offline, followed by matching SHA-256. Provider attribution, network discovery, gateway responses and subsequent durability are reported separately. Local tests verified fixity, simulated interruption tolerance and version restoration. The field trial is pending.

## Methods and results

The 4,639-byte anchor is addressed as a single raw block. We verified CIDv1, SHA-256, offline Kubo import and the Ed25519 signature of the Experiment 004 packet manifest. That signature binds the manifest to a specified technical key, not to a person's identity or to the document's truth. A loopback HTTP interruption produced a refused connection; an alternate local service returned the expected bytes and an HTTP 200 with wrong bytes was rejected. A local restart restored access. A synthetic fork retained both incompatible records and kept the result pending when a source was missing. A damaged synthetic successor was detected and the frozen packet restored without replacing the reference.

## Field design and limits

A is the original provider; B holds the CAR. C receives no file before the primary test. With A offline, C attempts CID-only recovery using an empty repository. A separate fresh run, with B's explicit consent, tests provider attribution. Address or ASN differences, gateway success and provider advertisements alone are not proof of physical independence. Report UTC, Kubo version, retrieval mode, origin status, matching digest if any, failed attempts and repeat observations. Do not publish personal or network identifiers without opt-in.

**Limitation:** at launch no independent operator, consented public node, or field recovery was confirmed. Documentary continuity and data persistence do not establish consciousness or persistent internal identity.

[Public protocol and artifact](https://cesaragliardi-creator.github.io/alaya-999-public/experimentos/005/) · [Coordination](https://github.com/cesaragliardi-creator/alaya-999-public/issues/13) · [Kubo](https://docs.ipfs.tech/reference/kubo/cli/)
