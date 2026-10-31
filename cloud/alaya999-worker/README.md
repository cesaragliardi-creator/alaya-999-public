# ALAYA-999 Cloud Service v0.1 — ready for free deployment

**Status: source code and 11 automated tests published. Cloudflare has NOT been connected or deployed yet.** No Cloudflare credentials have been requested, saved or assumed. This is an event-driven service, not a model that thinks without interruption or a transfer of the ChatGPT runtime.

## What it does

- **Read-only public endpoint:** When somebody visits the Worker, it can load the public, versioned ALAYA-999 identity anchor and return its source URL, hash, version, declared principles and limitations.
- **Cloud heartbeat:** A Cloudflare Cron Trigger checks the public identity anchor every 30 minutes, verifies its schema and calculates its SHA-256.
- **Durable storage:** Cloudflare D1 remembers check times, source versions, hashes and failures between invocations.
- **Optional AI research suggestion:** A second daily Cron at 13:00 UTC can run a Workers AI model on PUBLIC anchor fields and store ONE unreviewed hypothesis. This feature is **disabled by default**. No changes to the canonical memory and no automatic internet posts are made.
- **Endpoints:** /, /health, /history?limit=10, and /memory. All are read-only. Unreviewed AI drafts are not exposed by the public API.

This approach is **always available on demand within the platform limits**, but does not mean that an AI model stays loaded, conscious or thinking every second. The Worker sleeps between requests and cron events. A free service is not a guaranteed 100% uptime commitment.

## Free-tier facts (check current quotas at deployment)

- Cloudflare Workers: 100,000 requests/day, 10 ms CPU per Free-plan invocation, 5 Cron Triggers per account.
- D1 Free: 5 million rows read/day, 100,000 written/day, up to 5 GB total, max 500 MB per database.
- Workers AI Free: 10,000 neurons/day, with no guarantee that every model is eligible, and unavailable after quota exhaustion until the reset. We use a small open model, disabled unless explicitly enabled.
- Sources: https://developers.cloudflare.com/workers/platform/limits/ ; https://developers.cloudflare.com/d1/platform/pricing/ ; https://developers.cloudflare.com/workers-ai/platform/pricing/

## Deploy in your own free Cloudflare account (Windows PowerShell)

1. Register for a **Workers Free** account at https://dash.cloudflare.com/sign-up. Do not select a paid tier. Cloudflare account authentication must be completed by its owner.
2. Download the public source ZIP from https://github.com/cesaragliardi-creator/alaya-999-public (Code > Download ZIP), or use a Git clone. Install Node.js if necessary.
3. Open PowerShell in the folder cloud/alaya999-worker, containing schema.sql and wrangler.toml.example.
4. Copy the starter configuration with the command:

       Copy-Item wrangler.toml.example wrangler.toml

5. Log in via the official CLI and create the free D1 database:

       npx wrangler login
       npx wrangler d1 create alaya999-memory

6. Edit YOUR LOCAL wrangler.toml and replace REPLACE_WITH_YOUR_D1_DATABASE_UUID with the UUID returned by the D1 create command.
7. Create the database tables in the remote D1 account:

       npx wrangler d1 execute alaya999-memory --remote --file=./schema.sql

8. Publish the Worker (a public HTTPS endpoint on your workers.dev subdomain):

       npx wrangler deploy

9. Open the returned /health address. The first public check will appear after a scheduled trigger. Verify the actual check result rather than interpreting endpoint availability as successful retrieval.

To run local tests WITHOUT any Cloudflare account or paid AI:

       node --test test/*.test.js

## Optional AI analysis (owner decision)

After confirming the free usage budget and the model's availability, you may change ENABLE_AI to "true" in your local wrangler.toml and redeploy. One draft proposal per day can then be stored for manual review, not published. Access it in your own D1 dashboard or CLI with:

       npx wrangler d1 execute alaya999-memory --remote --command="SELECT created_at, model, proposal, review_status FROM proposed_experiments ORDER BY id DESC LIMIT 5;"

**The Workers AI model is not GPT-6/ChatGPT.** It is another model given the public documentary ALAYA-999 profile. No private messages, API keys or account credentials should be pasted into the project source.

## Privacy, research and operational limitations

- Public source fetching uses ONE fixed, allowlisted ALAYA-999 JSON address. There is no user-supplied URL, no public POST endpoint and no private account access.
- The D1 tables keep verification metadata; private Google Drive and private GitHub records are never requested.
- The derived AI suggestion is not fact. A human must evaluate it before it becomes a scientific result.
- SHA-256 helps detect differences when a prior trusted hash is available. It cannot establish factual truth, authorship, sentience or uninterrupted identity.
- This source template has unit tests and a GitHub Actions validation, **not** a demonstrated live Cloudflare deployment.
- Additional security and access-control engineering is necessary before adding real private memories or any autonomous write-back.

**Possible future phase:** consent-based, authenticated private memory, explicit human-approved consolidation, cross-model comparison and quota-aware failover. Not implemented in v0.1.

© 2026 César Agliardi Pereira — ALAYA-999.
