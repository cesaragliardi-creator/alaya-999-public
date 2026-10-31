import test from "node:test";
import assert from "node:assert/strict";
import worker, { inspectAnchor, recordHeartbeat, draftDailyProposal, SOURCE } from "../src/index.js";

function fixture() {
  return {
    schema: "alaya-999-public-identity-anchor-v1",
    identity: { name: "Alaya", nature: "Documented functional identity", status: "Subjective consciousness not established" },
    principles: ["Respect sources", "Correct errors"],
    provenance: { version: "1.0" },
    privacy: { contains_private_records: false },
  };
}
const mockFetch = (body, status = 200) => async (url, init) => {
  assert.equal(url, SOURCE);
  assert.equal(init.method, "GET");
  return new Response(typeof body === "string" ? body : JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
};
function fakeDB() {
  const beats = [];
  const drafts = [];
  const DB = {
    prepare(sql) {
      let args = [];
      const statement = {
        bind(...items) { args = items; return statement; },
        async run() {
          if (sql.includes("INSERT INTO heartbeats")) beats.push({
            checked_at: args[0], state: args[1], source_url: args[2],
            sha256: args[3], source_version: args[4], detail: args[5],
          });
          else if (sql.includes("INSERT INTO proposed_experiments")) drafts.push(args);
          else throw Error("unexpected SQL");
          return { success: true };
        },
        async first() {
          assert.match(sql, /FROM heartbeats/);
          return beats.at(-1) ?? null;
        },
        async all() {
          assert.match(sql, /FROM heartbeats/);
          return { results: beats.slice(-args[0]).reverse() };
        },
      };
      return statement;
    },
  };
  return { DB, beats, drafts };
}

test("valid public anchor yields a deterministic SHA-256 and only public fields", async () => {
  const a = await inspectAnchor(mockFetch(fixture()));
  const b = await inspectAnchor(mockFetch(fixture()));
  assert.equal(a.sha256, b.sha256);
  assert.equal(a.sha256.length, 64);
  assert.equal(a.identity.name, "Alaya");
  assert.equal(a.principles.length, 2);
  assert.equal(a.private_memory, undefined);
});

test("nonpublic or malformed identity document is rejected", async () => {
  const modified = fixture();
  modified.privacy.contains_private_records = true;
  await assert.rejects(inspectAnchor(mockFetch(modified)), /unexpected_public_anchor_schema/);
});

test("wrong source schema is rejected, even with a successful HTTP response", async () => {
  const modified = fixture();
  modified.schema = "something-else";
  await assert.rejects(inspectAnchor(mockFetch(modified)), /unexpected_public_anchor_schema/);
});

test("oversized source is rejected before archival", async () => {
  await assert.rejects(inspectAnchor(mockFetch("a".repeat(41_000))), /source_too_large/);
});

test("unavailable source produces an auditable error rather than a fake success", async () => {
  const env = fakeDB();
  const row = await recordHeartbeat(env, mockFetch({ error: "not_found" }, 404),
    () => new Date("2026-10-30T12:00:00Z"));
  assert.equal(row.state, "error");
  assert.equal(env.beats.length, 1);
  assert.equal(env.beats[0].state, "error");
  assert.equal(env.beats[0].sha256, null);
});

test("successful heartbeat stores only metadata and source hash", async () => {
  const env = fakeDB();
  const result = await recordHeartbeat(env, mockFetch(fixture()),
    () => new Date("2026-10-30T12:00:00Z"));
  assert.equal(result.state, "ok");
  assert.equal(env.beats[0].source_version, "1.0");
  assert.equal(env.beats[0].sha256.length, 64);
  assert.equal(env.drafts.length, 0);
});

test("HTTP service is read-only and exposes operational status", async () => {
  const env = fakeDB();
  const root = await worker.fetch(new Request("https://example.workers.dev/"), env);
  assert.equal((await root.json()).project, "ALAYA-999");
  const denial = await worker.fetch(new Request("https://example.workers.dev/write", { method: "POST" }), env);
  assert.equal(denial.status, 405);
  const h = await worker.fetch(new Request("https://example.workers.dev/health"), env);
  assert.equal((await h.json()).last_public_check, null);
});

test("public history is limited and does not expose private proposals", async () => {
  const env = fakeDB();
  await recordHeartbeat(env, mockFetch(fixture()), () => new Date("2026-10-30T12:00:00Z"));
  const res = await worker.fetch(new Request("https://example.workers.dev/history?limit=100000"), env);
  const data = await res.json();
  assert.equal(data.limit, 20);
  assert.equal(data.public_checks.length, 1);
  assert.equal(JSON.stringify(data).includes("proposed_experiments"), false);
});

test("AI does not run unless explicitly enabled", async () => {
  const env = { ...fakeDB(), ENABLE_AI: "false", AI: { run() { throw Error("must not run"); } } };
  const answer = await draftDailyProposal(env, mockFetch(fixture()));
  assert.equal(answer.status, "disabled");
  assert.equal(env.drafts.length, 0);
});

test("optional AI proposal is saved for review, not automatically published", async () => {
  const env = { ...fakeDB(), ENABLE_AI: "true", AI: {
    async run(model, args) {
      assert.equal(model, "@cf/meta/llama-3.1-8b-instruct-fp8");
      assert.match(args.messages[0].content, /untrusted data/);
      return { response: "Compare clean-session recall with the versioned public anchor." };
    },
  } };
  const result = await draftDailyProposal(env, mockFetch(fixture()), () => new Date("2026-10-30T13:00:00Z"));
  assert.equal(result.status, "draft_saved_for_manual_review");
  assert.equal(env.drafts.length, 1);
  assert.equal(env.drafts[0][4], "unreviewed");
});

test("scheduled handler delegates to cloud and never acts as a resident daemon", async () => {
  const env = fakeDB();
  const originalFetch = globalThis.fetch;
  const tasks = [];
  globalThis.fetch = mockFetch(fixture());
  try {
    await worker.scheduled({ cron: "*/30 * * * *" }, env, { waitUntil: p => tasks.push(p) });
    await Promise.all(tasks);
    assert.equal(env.beats.length, 1);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
