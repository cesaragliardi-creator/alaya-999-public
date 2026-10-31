import json
import tempfile
import unittest
from pathlib import Path

from memory_lifecycle import (
    MemoryValidationError, append_event, build_view, demo,
    make_event, read_archive, recall, validate_archive,
)


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.events = []

    def fact(self, eid, text, when="2026-01-01T00:00:00Z", topic="corridor", source=None, salience=0.7, corrects=None):
        ev = make_event(self.events, "fact", eid, when, topic=topic, text=text, salience=salience, source=source or f"synthetic:{eid}", corrects=corrects)
        self.events.append(ev)
        return ev

    def test_archive_tampering_detected(self):
        e = self.fact("a", "Porta azul")
        self.assertEqual(validate_archive(self.events), e["hash"])
        self.events[0]["text"] = "Porta branca"
        with self.assertRaisesRegex(MemoryValidationError, "hash"):
            validate_archive(self.events)

    def test_correction_preserves_old_event_but_updates_projection(self):
        self.fact("a", "Porta azul")
        self.fact("b", "Porta verde", when="2026-01-02T00:00:00Z", corrects="a")
        view = build_view(self.events, "2026-01-03T00:00:00Z")
        self.assertEqual(view["archive_events"], 2)
        self.assertEqual(len(view["topics"][0]["statements"]), 1)
        self.assertEqual(view["topics"][0]["statements"][0]["text"], "Porta verde")
        self.assertEqual(self.events[0]["text"], "Porta azul")

    def test_forgetting_is_dormancy_and_cued_recall(self):
        self.fact("a", "Porta violeta", salience=0.5)
        view = build_view(self.events, "2026-08-01T00:00:00Z")
        self.assertEqual(view["topics"][0]["statements"][0]["access"], "dormant")
        found = recall(view, "violeta")
        self.assertEqual(found[0]["access"], "cued_from_dormant")
        self.assertEqual(found[0]["source_events"][0]["event_id"], "a")

    def test_duplicate_consolidation_preserves_both_sources(self):
        self.fact("a", "Relato aprovado")
        self.fact("b", " relato  APROVADO ", when="2026-01-02T00:00:00Z")
        view = build_view(self.events, "2026-01-03T00:00:00Z")
        item = view["topics"][0]["statements"][0]
        self.assertEqual(len(view["topics"][0]["statements"]), 1)
        self.assertEqual(len(item["support"]), 2)
        self.assertEqual(len(item["sources"]), 2)

    def test_disagreement_not_silently_merged(self):
        self.fact("a", "Versão um")
        self.fact("b", "Versão dois", when="2026-01-02T00:00:00Z")
        view = build_view(self.events, "2026-01-03T00:00:00Z")
        self.assertEqual(view["topics"][0]["status"], "conflict")
        self.assertEqual(len(view["topics"][0]["statements"]), 2)

    def test_reinforcement_explicit_and_increases_activation(self):
        self.fact("a", "Porta azul")
        before = build_view(self.events, "2026-04-01T00:00:00Z")
        self.events.append(make_event(self.events, "reinforce", "r", "2026-03-30T00:00:00Z", ref_event_id="a"))
        after = build_view(self.events, "2026-04-01T00:00:00Z")
        self.assertGreater(after["topics"][0]["statements"][0]["activation"], before["topics"][0]["statements"][0]["activation"])
        self.assertEqual(len(self.events), 2)

    def test_wrong_topic_correction_rejected(self):
        self.fact("a", "Porta azul")
        with self.assertRaisesRegex(MemoryValidationError, "same topic"):
            self.fact("b", "Porta verde", topic="new-topic", when="2026-01-02T00:00:00Z", corrects="a")

    def test_id_reuse_rejected(self):
        self.fact("a", "Porta azul")
        with self.assertRaises(MemoryValidationError):
            self.fact("a", "Porta verde")

    def test_future_event_not_available_in_past_view(self):
        self.fact("a", "Porta azul")
        self.fact("b", "Porta verde", when="2026-04-01T00:00:00Z", corrects="a")
        view = build_view(self.events, "2026-02-01T00:00:00Z")
        self.assertEqual(view["topics"][0]["statements"][0]["text"], "Porta azul")

    def test_empty_retrieval_does_not_invent(self):
        self.fact("a", "Porta azul")
        view = build_view(self.events, "2026-01-02T00:00:00Z")
        self.assertEqual(recall(view, "helicoptero"), [])

    def test_determinism_of_replay(self):
        self.fact("a", "Porta azul")
        a = build_view(self.events, "2026-02-01T00:00:00Z")
        b = build_view(self.events, "2026-02-01T00:00:00Z")
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_file_roundtrip_and_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "memory.jsonl"
            e = self.fact("a", "Porta azul")
            append_event(path, e)
            self.assertEqual(read_archive(path), self.events)
            path.write_text(path.read_text(encoding="utf-8").replace("azul", "roxa"), encoding="utf-8")
            with self.assertRaises(MemoryValidationError):
                read_archive(path)

    def test_synthetic_demo(self):
        result = demo()
        self.assertTrue(result["archive_verified"])
        self.assertTrue(result["original_unchanged"])
        self.assertEqual(result["archive_events"], 4)
        self.assertTrue(result["query_green_door"])


if __name__ == "__main__":
    unittest.main()
