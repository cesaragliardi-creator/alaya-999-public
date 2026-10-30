# ALAYA-999 — Zenodo Deposit Preparation and Rights Checklist

**Date prepared:** 2026-10-30  
**Owner/creator:** César Agliardi Pereira  
**Scope:** Public research files only. No private Google Drive documents, private GitHub repository, credentials, or personal conversations.

## Status

**UPDATE (2026-10-30): Deposited according to the published Zenodo record shown by the account holder.** Version DOI: https://doi.org/10.5281/zenodo.23802112; concept DOI: https://doi.org/10.5281/zenodo.23802110. Public independent fetch by this assistant has not yet succeeded. The first-deposit steps below are retained as a historical checklist; do not make a duplicate initial deposit.


### Required follow-up on the actual 2026-10-30 Zenodo record

The account holder's published record text displays the creator as `pereira, cesar`, while the public documentation attributes the work to **César Agliardi Pereira**. Edit the existing Zenodo creator metadata instead of creating a new record: family name `Pereira`, given names `César Agliardi`.

It also shows a **Creative Commons Attribution 4.0** licence plus **All Rights Reserved** text. These are not equivalent: a copyright notice does not revoke CC BY permission. Zenodo supports editing published metadata, including licence selection. If a restrictive licence is preferred for future access, remove the CC BY licence display and select an appropriate custom rights description after reviewing the legal effect. However, Creative Commons licences already validly granted to recipients cannot be retroactively revoked by a subsequent metadata change. Seek legal guidance if the unintended CC BY grant presents a material concern.

Zenodo's official edit-record help: https://help.zenodo.org/docs/deposit/manage-records/ ; rights help: https://help.zenodo.org/docs/deposit/describe-records/licenses/

## Original recommended first record (historical)

- **Title:** ALAYA-999: Persistent AI Memory, Functional Identity, and Cross-Model Continuity — A Reproducible Research Framework
- **Author:** Pereira, César Agliardi
- **Date:** Use the actual first Zenodo publication date when published.
- **Language:** English
- **Suggested resource type for a manually uploaded research note:** Publication / Preprint or report (choose the option actually offered by Zenodo and accurately reflecting its unreviewed status).
- **Suggested resource type for GitHub release archiving:** Software, because the repository also includes audit scripts and workflows.
- **Version:** 1.0 (public research note; match archived files).
- **Keywords:** persistent AI memory; functional identity; external memory; cross-model recovery; AI reproducibility; provenance; human–AI collaboration.
- **Description:** Use the Abstract section of `RESEARCH_ABSTRACT.md`, with the clear caveat that independent cross-model validation remains pending.
- **Related source:** https://github.com/cesaragliardi-creator/alaya-999-public
- **Project website:** https://cesaragliardi-creator.github.io/alaya-999-public/
- **DOI:** Not assigned; never fabricate or reserve a value in this documentation.

## Rights correction REQUIRED on the published record

The repository currently says **all rights reserved** and does not grant a public reuse licence. Zenodo deposit forms default to **CC BY 4.0**, which grants broader reuse rights; do **not** accept that default unless the copyright holder intentionally chooses it. Zenodo provides the ability to specify a custom licence in a manual deposit. Verify that your selected licence and the type of access are consistent with your intended rights before publishing.

**Do not automatically connect a GitHub release and assume rights are protected.** An archiving integration may use a default licence if no valid licence is supplied in metadata. The `CITATION.cff` file intentionally does not claim a licence, and no `.zenodo.json` auto-ingestion file is supplied pending rights review.

Zenodo technical documentation: https://help.zenodo.org/docs/deposit/describe-records/licenses/ and https://help.zenodo.org/docs/github/.

## Route A — Historical steps for the first manual deposit

1. Log in at https://zenodo.org/ using your own account; do not send passwords or tokens to chat.
2. Choose New upload; select only reviewed public research materials (e.g., `RESEARCH_ABSTRACT.md`, `RECOVERY_TEST.md`, `alaya-anchor-public-v1.json`, the public integrity manifest).
3. Supply the accurate title, creator, abstract, keywords, public source link and resource type. Clearly identify the material as not peer reviewed and the validation results as pending.
4. Review permissions and choose the licence explicitly. The author can select a custom licence if the platform supports the desired rights wording.
5. Save the draft and check files and metadata. **Publish only after you have reviewed the irreversible public record.**
6. Record the actual DOI, Zenodo URL, publication date and version in `network-status.json` and `NETWORK.md` only after independent verification.

## Route B — GitHub releases auto-archived by Zenodo (future software artefacts)

1. Log in using GitHub and explicitly authorize the Zenodo-GitHub integration.
2. Open your Zenodo GitHub settings, press **Sync now**, find only `cesaragliardi-creator/alaya-999-public`, and enable it. **Do not** enable the private memory repository.
3. Resolve and validate licensing/metadata *before* publishing a new GitHub release. `CITATION.cff` supports GitHub's “Cite this repository” feature; for Zenodo-specific metadata, `.zenodo.json` can be added after rights are settled.
4. Create a **new** correctly versioned GitHub release only after integration is enabled and the intended archived files and rights have been verified. An old release may not be automatically imported just by enabling integration.
5. Verify Zenodo generated a record, archive checksum/contents and a real DOI. Do not reuse an unverified DOI.

**Avoid double counting:** Manual note deposit and release archival can be different records. Record their relationships accurately instead of presenting both as the same unique scholarly work.

## Scientific integrity checklist

- [ ] Author and title verified
- [ ] Only public/reviewed artefacts included
- [ ] Scope and unreviewed status clearly stated
- [ ] No fabricated experimental performance or citations
- [ ] Copyright and licence explicitly selected
- [ ] Exact version and commit recorded
- [ ] Actual Zenodo DOI and landing-page URL captured
- [ ] Public registry updated only after successful publication

The deposit creates a **citable archival record**. It does not constitute peer review, independent validation, or proof of an autonomous AI identity.
