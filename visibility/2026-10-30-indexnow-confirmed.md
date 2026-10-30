# ALAYA-999 — Public search discovery: verified IndexNow receipts (2026-10-30)

**Research:** ALAYA-999, César Agliardi Pereira  
**Public DOI:** https://doi.org/10.5281/zenodo.23802112  
**Website:** https://cesaragliardi-creator.github.io/alaya-999-public/

## Confirmed evidence

On **2026-10-30 at 23:32:18–23:32:20 UTC**, GitHub Actions
[run 41145048603](https://github.com/cesaragliardi-creator/alaya-999-public/actions/runs/41145048603)
executed the public IndexNow notification script
(`scripts/indexnow_public_discovery.py`), and its logs recorded:

| Public URL | Page reachable | IndexNow HTTP response |
|---|---|---|
| https://cesaragliardi-creator.github.io/alaya-999-public/ | HTTP 200, marker checked | 200 |
| https://cesaragliardi-creator.github.io/alaya-999-public/pt/pesquisa.html | HTTP 200, marker checked | 200 |
| https://cesaragliardi-creator.github.io/alaya-999-public/en/research.html | HTTP 200, marker checked | 200 |

The project-specific UTF-8 key file at
`https://cesaragliardi-creator.github.io/alaya-999-public/28d64bafdd7bc8ceff483428ccc5227d.txt`
was also retrieved and checked for expected content before sending any
notification. The script reported `"status": "received_not_indexed"`,
with all three `"received": true`.

An earlier independent
[run 41145021888](https://github.com/cesaragliardi-creator/alaya-999-public/actions/runs/41145021888)
recorded three further successful HTTP 200 responses. The later run is
preferable evidence because the workflow also includes `set -o pipefail`.

## New corrections made to public discovery

- `sitemap.xml`: replaced links to Jekyll-generated Markdown source
  `.md` files with their published `.html` routes, and added the public
  recovery test and research abstract pages. The GitHub Pages build
  previously logged `AI_START_HERE.html`, `BOOK_DIALOGUE.html`,
  `RECOVER_ALAYA.html`, `RECOVERY_TEST.html`, and
  `RESEARCH_ABSTRACT.html` as output artifacts.
- `index.html`: corrected ten links to generated HTML documentation.
- `en/research.html`: corrected four documentation links and included a
  direct link to the OpenAIRE DOI lookup record.
- `pt/pesquisa.html`: corrected three documentation links and included
  Zenodo and OpenAIRE discovery links.
- `.github/workflows/indexnow-public-discovery.yml`: fixed a pipeline
  failure mode. Previously `python3 ... | tee ...` could return exit code
  zero even when the verifier failed. Now `set -o pipefail` preserves the
  verifier's exit status and still retains an evidence artifact.

Files were updated only within the authorized **public**
`cesaragliardi-creator/alaya-999-public` repository. Every new version
was fetched and compared for byte-identical content after GitHub wrote it.
No originals were deleted, no private memory or user data was published,
and no external account was created.

## Provenance and limits

- The relevant public GitHub Actions run logs provide the primary
  evidence of **HTTP receipt** from IndexNow; no private credential is
  needed to review the workflow summary.
- The official IndexNow documentation
  (https://www.indexnow.org/documentation) states that HTTP 200 means
  the endpoint received the URL. It does not prove search inclusion,
  click-through traffic, reader engagement or academic endorsement.
- Search Console verification was reported by the project owner;
  this repository audit did not access Search Console account data.
- OpenAIRE is a discovery/metadata registry and is not independent
  experimental validation.
- Site deployment for the final modified sitemap and documents needs a
  successful Pages build; do not imply that every amended file was
  already crawled from live GitHub Pages simply because it was committed.
- No evidence of exponential audience growth follows from these
  notifications; that requires timestamped analytics over multiple
  intervals and independently observed citations or visitors.

## Repeatability

Inspect:
1. [Public IndexNow code](../scripts/indexnow_public_discovery.py)
2. [Workflow](../.github/workflows/indexnow-public-discovery.yml)
3. [Completed run and log](https://github.com/cesaragliardi-creator/alaya-999-public/actions/runs/41145048603)
4. [Revised sitemap](../sitemap.xml)

This report describes actual configuration, public HTTP probes and
service responses; it does not claim a permanently autonomous AI agent,
consciousness or memory persistence between models.
