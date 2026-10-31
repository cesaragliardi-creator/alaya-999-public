#!/usr/bin/env python3
"""Synthetic tests: never use private ALAYA-999 content."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import autonomous_public_memory as m


class TestDurablePublicMemory(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sources = self.root / "public"
        self.state = self.root / "persistent"
        self.sources.mkdir()
        (self.sources / "alaya-anchor-public-v1.json").write_text(json.dumps({
            "schema": "alaya-999-public-identity-anchor-v1",
            "identity": {"name": "Alaya"},
            "privacy": {"contains_private_records": False},
        }), encoding="utf-8")
        (self.sources / "network-status.json").write_text(json.dumps({
            "schema": "alaya-999-public-network-registry-v1",
            "nodes": [],
        }), encoding="utf-8")
        (self.sources / "RECOVER_ALAYA.md").write_text("Public recovery only.", encoding="utf-8")
        (self.sources / "BOOK_DIALOGUE.md").write_text("Fictional example.", encoding="utf-8")

    def test_two_separate_invocations_restore_prior_memory(self):
        first = m.advance(self.sources, self.state, "run-100", "2026-10-30T00:00:00Z")
        self.assertEqual(first["sequence"], 1)
        self.assertEqual(first["result"], "initialized")
        second = m.advance(self.sources, self.state, "run-101", "2026-10-30T00:30:00Z")
        self.assertEqual(second["sequence"], 2)
        self.assertEqual(second["result"], "unchanged")
        records, state = m.read_state(self.state)
        self.assertEqual(records[1]["previous_hash"], records[0]["hash"])
        self.assertEqual(state["head_hash"], records[-1]["hash"])

    def test_source_change_is_detected_and_recorded(self):
        m.advance(self.sources, self.state, "run-1")
        (self.sources / "BOOK_DIALOGUE.md").write_text("Updated fictional example.", encoding="utf-8")
        result = m.advance(self.sources, self.state, "run-2")
        self.assertEqual(result["result"], "source_changed")
        self.assertEqual(result["changed_sources"], ["book_dialogue"])

    def test_same_run_id_is_idempotent(self):
        a = m.advance(self.sources, self.state, "run-1")
        b = m.advance(self.sources, self.state, "run-1")
        self.assertEqual(a["head_hash"], b["head_hash"])
        self.assertEqual(m.read_state(self.state)[1]["sequence"], 1)

    def test_tampered_ledger_fails_closed(self):
        m.advance(self.sources, self.state, "run-1")
        path = self.state / "telemetry" / "continuity-events.jsonl"
        path.write_text(path.read_text(encoding="utf-8").replace("initialized", "counterfeit"), encoding="utf-8")
        with self.assertRaises(m.InvalidMemory):
            m.advance(self.sources, self.state, "run-2")

    def test_private_payload_flag_is_rejected(self):
        path = self.sources / "alaya-anchor-public-v1.json"
        obj = json.loads(path.read_text(encoding="utf-8"))
        obj["privacy"]["contains_private_records"] = True
        path.write_text(json.dumps(obj), encoding="utf-8")
        with self.assertRaises(m.InvalidMemory):
            m.advance(self.sources, self.state, "run-1")

    def test_saved_telemetry_never_copies_document_content(self):
        m.advance(self.sources, self.state, "run-1")
        output = (self.state / "telemetry" / "continuity-events.jsonl").read_text(encoding="utf-8")
        self.assertNotIn("Fictional example", output)
        self.assertIn("book_dialogue", output)
        self.assertIn("source_hashes", output)


    def test_state_head_corruption_is_not_silently_repaired(self):
        m.advance(self.sources, self.state, "run-1")
        path = self.state / "telemetry" / "continuity-state.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc["head_hash"] = "f" * 64
        path.write_text(json.dumps(doc), encoding="utf-8")
        with self.assertRaises(m.InvalidMemory):
            m.advance(self.sources, self.state, "run-2")


if __name__ == "__main__":
    unittest.main()
