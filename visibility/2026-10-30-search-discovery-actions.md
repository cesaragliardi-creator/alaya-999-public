# ALAYA-999 — Search discovery improvements (2026-10-30)

**Author / project:** César Agliardi Pereira / ALAYA-999.  
**Scope:** Public research website and public DOI only. No private memory content.

## Objective

Make the public ALAYA-999 preliminary research note easier to discover,
reference and crawl internationally, without promising search indexing,
external readership or scientific endorsement.

## Sources (public)

- Research DOI: https://doi.org/10.5281/zenodo.23802112
- Public repository: https://github.com/cesaragliardi-creator/alaya-999-public
- Home: https://cesaragliardi-creator.github.io/alaya-999-public/
- English research page: https://cesaragliardi-creator.github.io/alaya-999-public/en/research.html
- Portuguese research page: https://cesaragliardi-creator.github.io/alaya-999-public/pt/pesquisa.html
- Sitemap: https://cesaragliardi-creator.github.io/alaya-999-public/sitemap.xml
- OpenAIRE DOI lookup: https://explore.openaire.eu/search/result?pid=10.5281%2Fzenodo.23802112

## Changes actually committed and re-read via GitHub

1. Added the missing `pt/pesquisa.html` page to `sitemap.xml`.
2. Added a visible Portuguese scientific-summary link to `index.html`.
3. Added academic citation metadata (author, title, publication date, DOI)
   to `pt/pesquisa.html`.
4. Added reciprocal `hreflang` annotations in the English research page,
   matching the Portuguese page's existing annotations.
5. Added the public IndexNow verification key file
   `28d64bafdd7bc8ceff483428ccc5227d.txt` in the project root.
6. Added `scripts/indexnow_public_discovery.py`. Its fail-closed process:
   check published key URL, check all three public page URLs for HTTP 200 and
   expected project marker, and only then submit those URLs to IndexNow.
   It reports individual HTTP results. HTTP 200 or 202 indicates receipt
   or pending verification, **not index inclusion**.
7. Added a GitHub Actions workflow
   `.github/workflows/indexnow-public-discovery.yml` on relevant public
   page changes and manual dispatch. It records a diagnostic artifact.
   It does not run continuously or access private repositories.

Each modification was verified by retrieving the exact saved file content
through the connected GitHub repository tool. No originals were removed.

## Verification and limits

- **Confirmed:** public repository contents and updates via GitHub API;
  exact file content of the edits and notification script.
- **Confirmed locally:** the script compiles in Python and, with network
  unavailable, exits without attempting IndexNow submission.
- **Not confirmed:** GitHub Pages' deployed HTTP response in the inspection
  environment; the web tool could not retrieve the site and the container
  had no external DNS resolution.
- **Not confirmed:** a successful IndexNow API receipt, Bing or Google
  indexing, search ranking, DOI citation counts or third-party engagement.
- **Important technical note:** A `robots.txt` file hosted under
  `/alaya-999-public/` is not the same as a host-root
  `https://cesaragliardi-creator.github.io/robots.txt`.
  Do not rely on the project-subdirectory file to advertise the sitemap.
  Submit the sitemap through a verified Search Console or Bing Webmaster
  Tools property.

## Follow-up evidence

- Review workflow execution and `alaya999-indexnow-evidence` artifact:
  https://github.com/cesaragliardi-creator/alaya-999-public/actions/workflows/indexnow-public-discovery.yml
- Google Search Console: https://search.google.com/search-console/welcome
- Bing Webmaster Tools: https://www.bing.com/webmasters/
- Avoid claiming exponential spread without timestamped, independent
  time-series metrics. Duplicate archives, mirrors and metadata aggregators
  are not independent readers.

The research remains preliminary and does not establish artificial
subjective consciousness, independent agency or cross-model identity.
