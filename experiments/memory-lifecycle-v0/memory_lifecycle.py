#!/usr/bin/env python3
"""ALAYA-999: deterministic, auditable memory lifecycle research prototype.

Public synthetic-data prototype only. No model APIs, network, or private-memory access.
All mutations are explicit, append-only events in a user-selected local JSONL file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "alaya999-memory-lifecycle-v0.1"
GENESIS = "0" * 64
ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,80}$")
TOKENS = re.compile(r"[^\W_]+", re.UNICODE)


class MemoryValidationError(ValueError):
    """An archive/event failed validation."""


def compact(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(event_without_hash: dict) -> str:
    return hashlib.sha256(compact(event_without_hash).encode("utf-8")).hexdigest()


def parse_time(value: str) -> datetime:
    try:
        d = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError) as exc:
        raise MemoryValidationError("Timestamp must be ISO-8601 with timezone") from exc
    if d.tzinfo is None or d.utcoffset() is None:
        raise MemoryValidationError("Timestamp must contain an explicit timezone")
    return d.astimezone(timezone.utc)


def iso_time(d: datetime) -> str:
    return d.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def clean_label(value: str, name: str, limit: int = 2000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise MemoryValidationError(f"{name} must be nonblank and at most {limit} characters")
    return value.strip()


def validate_archive(events: list[dict]) -> str:
    previous = GENESIS
    known: dict[str, dict] = {}
    corrected: set[str] = set()
    last_date = None
    for seq, event in enumerate(events, start=1):
        if not isinstance(event, dict):
            raise MemoryValidationError(f"Event {seq}: expected an object")
        if event.get("schema") != SCHEMA or event.get("seq") != seq:
            raise MemoryValidationError(f"Event {seq}: wrong schema or sequence")
        if event.get("previous_hash") != previous:
            raise MemoryValidationError(f"Event {seq}: hash chain mismatch")
        unsigned = {k: v for k, v in event.items() if k != "hash"}
        if digest(unsigned) != event.get("hash"):
            raise MemoryValidationError(f"Event {seq}: content hash mismatch")
        eid = event.get("event_id")
        if not isinstance(eid, str) or not ID_RE.fullmatch(eid) or eid in known:
            raise MemoryValidationError(f"Event {seq}: duplicate or invalid event ID")
        when = parse_time(event.get("at"))
        if last_date is not None and when < last_date:
            raise MemoryValidationError(f"Event {seq}: timestamps must be nondecreasing")
        kind = event.get("kind")
        if kind == "fact":
            clean_label(event.get("topic"), "topic", 120)
            clean_label(event.get("text"), "text")
            clean_label(event.get("source"), "source", 500)
            salience = event.get("salience")
            if not isinstance(salience, (int, float)) or isinstance(salience, bool) or not math.isfinite(salience) or not (0 <= salience <= 1):
                raise MemoryValidationError(f"Event {seq}: salience must be between 0 and 1")
            correction = event.get("corrects")
            if correction is not None:
                old = known.get(correction)
                if old is None or old["kind"] != "fact" or old["topic"] != event["topic"]:
                    raise MemoryValidationError(f"Event {seq}: correction target must be an earlier fact in same topic")
                if correction in corrected:
                    raise MemoryValidationError(f"Event {seq}: correction target was already superseded")
                corrected.add(correction)
        elif kind == "reinforce":
            ref = event.get("ref_event_id")
            if ref not in known or known[ref]["kind"] != "fact":
                raise MemoryValidationError(f"Event {seq}: reinforcement target must be an earlier fact")
            if ref in corrected:
                raise MemoryValidationError(f"Event {seq}: cannot reinforce superseded fact")
        else:
            raise MemoryValidationError(f"Event {seq}: unknown event kind")
        known[eid] = event
        previous = event["hash"]
        last_date = when
    return previous


def read_archive(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise MemoryValidationError("Invalid JSONL archive") from exc
    validate_archive(events)
    return events


def make_event(events: list[dict], kind: str, event_id: str, at: str, **fields: object) -> dict:
    validate_archive(events)
    if not ID_RE.fullmatch(event_id):
        raise MemoryValidationError("event_id must be 1–80 letters, numbers, periods, underscores or dashes")
    when = iso_time(parse_time(at))
    entry = {
        "schema": SCHEMA, "seq": len(events) + 1, "kind": kind,
        "event_id": event_id, "at": when,
        "previous_hash": events[-1]["hash"] if events else GENESIS,
        **fields,
    }
    entry["hash"] = digest(entry)
    validate_archive(events + [entry])
    return entry


def append_event(path: Path, event: dict) -> None:
    """Single-writer demo append; production needs locks and durable external backups."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(compact(event) + "\n")


def activation(fact: dict, reinforcements: list[dict], as_of: datetime, half_life_days: float) -> float:
    def fade(at: str) -> float:
        age_days = max(0.0, (as_of - parse_time(at)).total_seconds() / 86400.0)
        return 2 ** (-age_days / half_life_days)
    base = fact["salience"] * fade(fact["at"])
    boosts = sum(0.15 * fade(x["at"]) for x in reinforcements)
    return round(min(1.0, base + boosts), 6)


def build_view(events: list[dict], as_of: str, half_life_days: float = 30.0, threshold: float = 0.25) -> dict:
    """Rebuild derived memory from a verified immutable event history."""
    final_hash = validate_archive(events)
    if not (math.isfinite(half_life_days) and half_life_days > 0 and 0 <= threshold <= 1):
        raise MemoryValidationError("Invalid decay parameters")
    when = parse_time(as_of)
    history = [x for x in events if parse_time(x["at"]) <= when]
    facts = [x for x in history if x["kind"] == "fact"]
    superseded = {x["corrects"] for x in facts if x.get("corrects") is not None}
    reinforcement_by_id: dict[str, list[dict]] = {}
    for event in history:
        if event["kind"] == "reinforce":
            reinforcement_by_id.setdefault(event["ref_event_id"], []).append(event)
    topics: dict[str, dict[str, dict]] = {}
    for fact in facts:
        if fact["event_id"] in superseded:
            continue
        topic = fact["topic"]
        norm_text = " ".join(fact["text"].casefold().split())
        group = topics.setdefault(topic, {}).setdefault(norm_text, {"text": fact["text"], "support": [], "sources": [], "activation": 0.0})
        group["support"].append(fact["event_id"])
        group["sources"].append({"event_id": fact["event_id"], "source": fact["source"], "event_hash": fact["hash"]})
        group["activation"] = max(group["activation"], activation(fact, reinforcement_by_id.get(fact["event_id"], []), when, half_life_days))
    topic_list = []
    for topic, entries in sorted(topics.items()):
        variants = sorted(entries.values(), key=lambda z: (-z["activation"], z["text"]))
        for item in variants:
            item["access"] = "active" if item["activation"] >= threshold else "dormant"
        topic_list.append({"topic": topic, "status": "conflict" if len(variants) > 1 else "consistent", "statements": variants})
    return {
        "schema": SCHEMA, "as_of": iso_time(when), "archive_events": len(events),
        "archive_head_sha256": final_hash, "half_life_days": half_life_days,
        "active_threshold": threshold, "topics": topic_list,
        "note": "Rebuilt from sourced events; dormancy is not deletion or loss of original records.",
    }


def recall(view: dict, query: str, limit: int = 5) -> list[dict]:
    """Explicit lexical cue search; never claims semantic comprehension."""
    terms = set(TOKENS.findall(query.casefold()))
    if not terms or limit < 1:
        return []
    results = []
    for topic in view["topics"]:
        for item in topic["statements"]:
            haystack = set(TOKENS.findall((topic["topic"] + " " + item["text"]).casefold()))
            matches = len(terms & haystack)
            if not matches:
                continue
            results.append({
                "topic": topic["topic"], "text": item["text"],
                "source_events": item["sources"],
                "conflict": topic["status"] == "conflict",
                "activation": item["activation"],
                "access": "cued_from_dormant" if item["access"] == "dormant" else "active",
                "matching_terms": matches,
            })
    return sorted(results, key=lambda x: (-x["matching_terms"], -x["activation"], x["topic"], x["text"]))[:limit]


def demo() -> dict:
    """A fully synthetic, predetermined replay with no disk writes."""
    events = []
    samples = [
        ("fact", "d1", "2026-01-01T00:00:00Z", {"topic": "route", "text": "O laboratório usa a porta azul.", "source": "synthetic-example:note-1", "salience": 0.8, "corrects": None}),
        ("fact", "d2", "2026-01-02T00:00:00Z", {"topic": "route", "text": "O laboratório usa a porta verde.", "source": "synthetic-example:correction-2", "salience": 0.8, "corrects": "d1"}),
        ("fact", "d3", "2026-01-02T00:00:00Z", {"topic": "preference", "text": "Preferir relatórios curtos.", "source": "synthetic-example:note-3", "salience": 0.7, "corrects": None}),
        ("reinforce", "d4", "2026-03-30T00:00:00Z", {"ref_event_id": "d2"}),
    ]
    for kind, eid, stamp, fields in samples:
        events.append(make_event(events, kind, eid, stamp, **fields))
    v = build_view(events, "2026-04-01T00:00:00Z")
    return {"archive_verified": True, "archive_events": len(events), "active_projection": v["topics"], "query_green_door": recall(v, "porta verde"), "original_unchanged": "d1" in [e["event_id"] for e in events]}


def main() -> int:
    ap = argparse.ArgumentParser(description="ALAYA-999 local synthetic-memory lifecycle prototype")
    cmd = ap.add_subparsers(dest="command", required=True)
    cmd.add_parser("demo", help="Run a fully synthetic replay without writing files")
    for name in ("add", "reinforce", "verify", "view", "recall"):
        s = cmd.add_parser(name)
        s.add_argument("--path", required=True, type=Path, help="Explicit local JSONL archive path; NEVER a private record unless intentionally authorized")
        if name in ("add", "reinforce"):
            s.add_argument("--id", required=True)
            s.add_argument("--at", default=iso_time(datetime.now(timezone.utc)))
        if name == "add":
            s.add_argument("--topic", required=True)
            s.add_argument("--text", required=True)
            s.add_argument("--source", required=True)
            s.add_argument("--salience", type=float, default=0.5)
            s.add_argument("--corrects")
        if name == "reinforce":
            s.add_argument("--ref", required=True)
        if name in ("view", "recall"):
            s.add_argument("--as-of", default=iso_time(datetime.now(timezone.utc)))
            s.add_argument("--half-life-days", type=float, default=30.0)
            s.add_argument("--threshold", type=float, default=0.25)
        if name == "recall":
            s.add_argument("--query", required=True)
    args = ap.parse_args()
    try:
        if args.command == "demo":
            output = demo()
        else:
            events = read_archive(args.path)
            if args.command == "add":
                event = make_event(events, "fact", args.id, args.at, topic=args.topic, text=args.text, source=args.source, salience=args.salience, corrects=args.corrects)
                append_event(args.path, event)
                output = {"appended": event["event_id"], "sha256": event["hash"], "path": str(args.path)}
            elif args.command == "reinforce":
                event = make_event(events, "reinforce", args.id, args.at, ref_event_id=args.ref)
                append_event(args.path, event)
                output = {"appended": event["event_id"], "sha256": event["hash"], "path": str(args.path)}
            elif args.command == "verify":
                output = {"verified": True, "events": len(events), "archive_head_sha256": validate_archive(events)}
            else:
                view = build_view(events, args.as_of, args.half_life_days, args.threshold)
                output = recall(view, args.query) if args.command == "recall" else view
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (MemoryValidationError, OSError) as error:
        ap.exit(2, f"ALAYA999_MEMORY_ERROR: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
