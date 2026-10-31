#!/usr/bin/env python3
"""Offline tests of network bootstrap verification; all content synthetic."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import bootstrap_alaya999 as b


class TestCrossModelBootstrap(unittest.TestCase):
    def make_sources(self):
        anchor = {
            "schema": "alaya-999-public-identity-anchor-v1",
            "identity": {
                "name": "Alaya",
                "description": "Synthetic independent identity test",
                "status": "No subjective identity claims",
            },
            "privacy": {"contains_private_records": False},
            "principles": ["Truth before agreement", "Document evidence"],
        }
        anchor_bytes = json.dumps(anchor, ensure_ascii=False).encode("utf-8")
        profile = {
            "schema": b.PROFILE_SCHEMA,
            "identity_name": "Alaya",
            "identity_description": anchor["identity"]["description"],
            "identity_status": anchor["identity"]["status"],
            "principles": anchor["principles"],
            "source_sha256": b.sha(anchor_bytes),
            "scope": "public_project_documentation_only",
        }
        e1 = {
            "schema": b.EVENT_SCHEMA, "seq": 1, "checked_at": "2026-10-30T00:00:00Z",
            "run_id": "run-001", "kind": "initialized",
            "source_hashes": {"identity_anchor": b.sha(anchor_bytes), "network": "publichash"},
            "changed_sources": ["identity_anchor", "network"],
            "previous_hash": b.GENESIS, "scope": "public_documentary_observation_only",
            "profile_snapshot": profile,
        }
        e1["hash"] = b.canonical_event_hash(e1)
        e2 = {
            "schema": b.EVENT_SCHEMA, "seq": 2, "checked_at": "2026-10-30T00:30:00Z",
            "run_id": "run-002", "kind": "unchanged",
            "source_hashes": e1["source_hashes"].copy(),
            "changed_sources": [],
            "previous_hash": e1["hash"], "scope": "public_documentary_observation_only",
        }
        e2["hash"] = b.canonical_event_hash(e2)
        state = {
            "schema": b.EVENT_SCHEMA, "sequence": 2,
            "head_hash": e2["hash"],
            "source_hashes": e2["source_hashes"].copy(),
            "last_checked_at": e2["checked_at"],
            "public_profile": copy.deepcopy(profile),
            "last_kind": "unchanged",
        }
        return {"anchor": anchor, "state": state, "events": [e1, e2]}

    @staticmethod
    def mock_fetch(sources):
        payload = {
            "anchor": json.dumps(sources["anchor"], ensure_ascii=False).encode(),
            "state": json.dumps(sources["state"], ensure_ascii=False).encode(),
            "events": "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in sources["events"]).encode(),
        }
        inverted = {v: k for k, v in b.URLS.items()}
        def fetch(url, limit):
            key = inverted[url]
            return payload[key]
        return fetch

    def test_two_run_provenance_is_recovered(self):
        d = self.make_sources()
        result = b.verify_bundle(self.mock_fetch(d))
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["event_sequence"], 2)
        self.assertEqual(result["identity"]["principles"], d["anchor"]["principles"])
        self.assertEqual(result["event_head_sha256"], d["events"][-1]["hash"])

    def test_detects_rewritten_event(self):
        d = self.make_sources()
        d["events"][0]["profile_snapshot"]["principles"][0] = "Falsified history"
        with self.assertRaises(b.BootstrapError):
            b.verify_bundle(self.mock_fetch(d))

    def test_rejects_mismatched_history_head(self):
        d = self.make_sources()
        d["state"]["head_hash"] = "f" * 64
        with self.assertRaises(b.BootstrapError):
            b.verify_bundle(self.mock_fetch(d))

    def test_rejects_private_anchor(self):
        d = self.make_sources()
        d["anchor"]["privacy"]["contains_private_records"] = True
        with self.assertRaises(b.BootstrapError):
            b.verify_bundle(self.mock_fetch(d))

    def test_rejects_changed_anchor_with_old_state(self):
        d = self.make_sources()
        d["anchor"]["principles"].append("New principle, not yet verified")
        with self.assertRaises(b.BootstrapError):
            b.verify_bundle(self.mock_fetch(d))

    def test_rejects_mismatched_public_profile(self):
        d = self.make_sources()
        d["state"]["public_profile"]["identity_status"] = "Invented claim"
        with self.assertRaises(b.BootstrapError):
            b.verify_bundle(self.mock_fetch(d))

    def test_rejects_missing_profile_snapshot(self):
        d = self.make_sources()
        d["events"][0].pop("profile_snapshot")
        d["events"][0]["hash"] = b.canonical_event_hash(d["events"][0])
        d["events"][1]["previous_hash"] = d["events"][0]["hash"]
        d["events"][1]["hash"] = b.canonical_event_hash(d["events"][1])
        d["state"]["head_hash"] = d["events"][1]["hash"]
        with self.assertRaises(b.BootstrapError):
            b.verify_bundle(self.mock_fetch(d))

    def test_unavailable_network_fails_closed(self):
        def no_network(url, limit):
            raise b.BootstrapError("not online")
        with self.assertRaises(b.BootstrapError):
            b.verify_bundle(no_network)

    def test_only_declared_public_source_urls(self):
        for key, url in b.URLS.items():
            self.assertEqual(url.split("/")[2], "raw.githubusercontent.com")
        with self.assertRaises(b.BootstrapError):
            b.https_fetch("http://example.com/private", 100)


if __name__ == "__main__":
    unittest.main()
