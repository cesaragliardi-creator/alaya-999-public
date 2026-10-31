#!/usr/bin/env python3
"""ALAYA-999 public, scheduled, source-grounded continuity observer.

Each separate invocation RE-READS a public repo snapshot and the previous
durable observation chain. Nothing here reads private memory, calls an AI,
rewrites canonical documents, or demonstrates continuous subjective thought.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "alaya-999-public-observer-v1"
GENESIS = "0" * 64
FILES = {
    "identity_anchor": "alaya-anchor-public-v1.json",
    "network": "network-status.json",
    "recovery_protocol": "RECOVER_ALAYA.md",
    "book_dialogue": "BOOK_DIALOGUE.md",
}
MAX_BYTES = 100_000
ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,120}$")


class InvalidMemory(ValueError):
    pass


def compact(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def object_hash(obj: dict) -> str:
    return sha(compact(obj).encode("utf-8"))


def observe_public_sources(root: Path) -> dict:
    result = {}
    for label, relative in FILES.items():
        source = root / relative
        data = source.read_bytes()
        if not data or len(data) > MAX_BYTES:
            raise InvalidMemory("missing or oversized public source: " + label)
        if label in ("identity_anchor", "network"):
            doc = json.loads(data)
            if label == "identity_anchor" and (
                doc.get("schema") != "alaya-999-public-identity-anchor-v1"
                or doc.get("identity", {}).get("name") != "Alaya"
                or doc.get("privacy", {}).get("contains_private_records") is not False
            ):
                raise InvalidMemory("invalid or unsafe public identity anchor")
            if label == "network" and doc.get("schema") != "alaya-999-public-network-registry-v1":
                raise InvalidMemory("invalid public network registry")
        result[label] = sha(data)
    return result


def event_hash(event: dict) -> str:
    return object_hash({k: v for k, v in event.items() if k != "hash"})


def read_state(root: Path):
    history_path = root / "telemetry" / "continuity-events.jsonl"
    state_path = root / "telemetry" / "continuity-state.json"
    if not history_path.exists() and not state_path.exists():
        return [], None
    if not history_path.exists() or not state_path.exists():
        raise InvalidMemory("state and history must both exist")
    try:
        events = [json.loads(line) for line in history_path.read_text(encoding="utf-8").splitlines() if line]
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise InvalidMemory("corrupt state encoding or JSON") from exc
    if not events or not isinstance(state, dict):
        raise InvalidMemory("incomplete state")
    last = GENESIS
    seen = set()
    for seq, item in enumerate(events, 1):
        if (item.get("schema") != SCHEMA or item.get("seq") != seq
            or item.get("previous_hash") != last
            or item.get("hash") != event_hash(item)
            or not isinstance(item.get("source_hashes"), dict)):
            raise InvalidMemory("memory chain integrity failed at event " + str(seq))
        run_id = item.get("run_id")
        if not isinstance(run_id, str) or run_id in seen:
            raise InvalidMemory("duplicate/invalid run ID")
        seen.add(run_id)
        last = item["hash"]
    if (state.get("schema") != SCHEMA or state.get("sequence") != len(events)
        or state.get("head_hash") != last
        or state.get("source_hashes") != events[-1]["source_hashes"]
        or state.get("last_checked_at") != events[-1]["checked_at"]):
        raise InvalidMemory("last memory state diverges from event chain")
    return events, state


def atomic_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(content, encoding="utf-8")
    os.replace(temp, path)


def advance(source_root: Path, state_root: Path, run_id: str, now: str | None = None) -> dict:
    if not ID_PATTERN.fullmatch(run_id):
        raise InvalidMemory("unsafe run ID")
    observed = observe_public_sources(source_root)
    events, previous = read_state(state_root)
    if any(e["run_id"] == run_id for e in events):
        return {"result": "idempotent", "sequence": len(events), "head_hash": events[-1]["hash"]}
    at = now or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    stamp = datetime.fromisoformat(at.replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise InvalidMemory("timestamp must include timezone")
    prior = previous["source_hashes"] if previous else {}
    changed = sorted(k for k, v in observed.items() if prior.get(k) != v)
    kind = "initialized" if not previous else ("source_changed" if changed else "unchanged")
    event = {
        "schema": SCHEMA,
        "seq": len(events) + 1,
        "checked_at": at,
        "run_id": run_id,
        "kind": kind,
        "changed_sources": changed,
        "source_hashes": observed,
        "previous_hash": events[-1]["hash"] if events else GENESIS,
        "scope": "public_documentary_observation_only",
    }
    event["hash"] = event_hash(event)
    current = {
        "schema": SCHEMA,
        "sequence": event["seq"],
        "last_checked_at": at,
        "head_hash": event["hash"],
        "source_hashes": observed,
        "last_kind": kind,
        "status": "observed",
        "limitation": "Scheduled external documentary memory; not continuous AI runtime or subjective identity.",
    }
    path = state_root / "telemetry"
    atomic_text(path / "continuity-events.jsonl", "".join(compact(e) + "\n" for e in [*events, event]))
    atomic_text(path / "continuity-state.json", json.dumps(current, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    # Verify the exact persisted representation, not just the in-memory objects.
    roundtrip_events, roundtrip_state = read_state(state_root)
    if len(roundtrip_events) != event["seq"] or roundtrip_state != current:
        raise InvalidMemory("persisted state did not round-trip")
    return {"result": kind, "sequence": event["seq"], "head_hash": event["hash"], "changed_sources": changed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--state-root", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    try:
        result = advance(args.source_root, args.state_root, args.run_id)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, "ALAYA-999 observer refused to overwrite state: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
