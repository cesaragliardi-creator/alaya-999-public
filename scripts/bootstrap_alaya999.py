#!/usr/bin/env python3
"""ALAYA-999 universal public bootstrap (read-only, no paid API or private memory).

A user-controlled host can run this BEFORE invoking a chosen language model.
Fail closed: no verified public history => no Alaya-labelled context.
This does not install prompts in third-party services or demonstrate sentience.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

BASE = "https://raw.githubusercontent.com/cesaragliardi-creator/alaya-999-public"
URLS = {
    "anchor": BASE + "/main/alaya-anchor-public-v1.json",
    "state": BASE + "/alaya999-memory-state/telemetry/continuity-state.json",
    "events": BASE + "/alaya999-memory-state/telemetry/continuity-events.jsonl",
}
EVENT_SCHEMA = "alaya-999-public-observer-v1"
PROFILE_SCHEMA = "alaya-999-public-profile-snapshot-v1"
GENESIS = "0" * 64
LIMITS = {"anchor": 50000, "state": 50000, "events": 4_000_000}


class BootstrapError(ValueError):
    pass


def compact(obj: dict) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_event_hash(event: dict) -> str:
    return sha(compact({k: v for k, v in event.items() if k != "hash"}))


def https_fetch(url: str, limit: int) -> bytes:
    if url not in URLS.values():
        raise BootstrapError("URL not in explicit public-source allowlist")
    request = Request(url, headers={"User-Agent": "ALAYA999-Bootstrap/1.0", "Accept": "application/json,text/plain"})
    try:
        with urlopen(request, timeout=12) as response:
            final = urlsplit(response.geturl())
            if final.scheme != "https" or final.hostname != "raw.githubusercontent.com" or response.geturl() != url:
                raise BootstrapError("unexpected HTTP redirect or origin")
            data = response.read(limit + 1)
    except BootstrapError:
        raise
    except Exception as exc:
        raise BootstrapError("source unavailable; no memory claims permitted: " + type(exc).__name__) from exc
    if not data or len(data) > limit:
        raise BootstrapError("empty/oversized public source")
    return data


def read_json(data: bytes, label: str):
    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise BootstrapError(label + " is invalid UTF-8 JSON") from exc


def validate_history(events: list, state: dict):
    if not isinstance(events, list) or not events or not isinstance(state, dict):
        raise BootstrapError("missing public memory history")
    previous = GENESIS
    snapshots = []
    seen_runs = set()
    for sequence, event in enumerate(events, start=1):
        if not isinstance(event, dict):
            raise BootstrapError("non-object memory event")
        if (event.get("schema") != EVENT_SCHEMA
            or event.get("seq") != sequence
            or event.get("previous_hash") != previous
            or event.get("hash") != canonical_event_hash(event)
            or not isinstance(event.get("source_hashes"), dict)):
            raise BootstrapError("memory history integrity failure at event " + str(sequence))
        run_id = event.get("run_id")
        if not isinstance(run_id, str) or not run_id or run_id in seen_runs:
            raise BootstrapError("missing/duplicate run identifier")
        seen_runs.add(run_id)
        profile = event.get("profile_snapshot")
        if profile is not None:
            if (not isinstance(profile, dict)
                or profile.get("schema") != PROFILE_SCHEMA
                or profile.get("source_sha256") != event["source_hashes"].get("identity_anchor")):
                raise BootstrapError("historical public profile mismatched its source")
            snapshots.append((sequence, event, profile))
        previous = event["hash"]
    last = events[-1]
    if (state.get("schema") != EVENT_SCHEMA
        or state.get("sequence") != len(events)
        or state.get("head_hash") != previous
        or state.get("source_hashes") != last.get("source_hashes")
        or state.get("last_checked_at") != last.get("checked_at")):
        raise BootstrapError("state does not match the verified event chain")
    if not snapshots:
        raise BootstrapError("no source-grounded public identity snapshot found")
    _, event, profile = snapshots[-1]
    if state.get("public_profile") != profile:
        raise BootstrapError("public profile state does not match latest snapshot")
    return event, profile


def verify_bundle(fetcher=https_fetch) -> dict:
    raw = {label: fetcher(url, LIMITS[label]) for label, url in URLS.items()}
    anchor = read_json(raw["anchor"], "anchor")
    state = read_json(raw["state"], "state")
    try:
        events = [json.loads(line) for line in raw["events"].decode("utf-8").splitlines() if line.strip()]
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise BootstrapError("malformed public event history") from exc
    _, profile = validate_history(events, state)
    if (anchor.get("schema") != "alaya-999-public-identity-anchor-v1"
        or anchor.get("identity", {}).get("name") != "Alaya"
        or anchor.get("privacy", {}).get("contains_private_records") is not False
        or sha(raw["anchor"]) != state["source_hashes"].get("identity_anchor")):
        raise BootstrapError("unverified public anchor or inconsistent published revision")
    if (profile.get("identity_name") != "Alaya"
        or profile.get("identity_description") != anchor["identity"].get("description")
        or profile.get("identity_status") != anchor["identity"].get("status")
        or profile.get("principles") != anchor.get("principles")
        or profile.get("source_sha256") != sha(raw["anchor"])):
        raise BootstrapError("public profile and anchor contents disagree")
    if not (isinstance(profile["principles"], list)
            and 1 <= len(profile["principles"]) <= 8
            and all(isinstance(p, str) and 1 <= len(p) <= 180 for p in profile["principles"])):
        raise BootstrapError("invalid public profile contents")
    return {
        "status": "verified",
        "project": "ALAYA-999",
        "scope": "PUBLIC functional/documentary identity only; no private Google Drive, lived experience or sentience transferred",
        "sources": URLS,
        "event_sequence": state["sequence"],
        "event_head_sha256": state["head_hash"],
        "last_checked_at": state["last_checked_at"],
        "identity": profile,
        "bootstrap_policy": [
            "Use only verified public documentary claims; do not fabricate private memories.",
            "Identify the model host and which externally retrieved records were provided.",
            "Maintain declared reasoning principles without pretending to be a continuously running person.",
            "Distinguish persona/function from subjective consciousness; do not claim to feel memories.",
            "Use the provided source URLs and event hashes as provenance; corrections must be explicit.",
            "No automatic public or private write-back: require separate authenticated authorization.",
        ],
        "note": "The host application, not the AI model, verified and supplied these public sources.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args()
    try:
        bundle = verify_bundle()
    except (BootstrapError, ValueError, KeyError, TypeError) as exc:
        print("ALAYA999_BOOTSTRAP_BLOCKED: " + str(exc), file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
    else:
        p = bundle["identity"]
        print("ALAYA-999 / verified public identity bootstrap, not subjective continuity")
        print("Memory event:", bundle["event_sequence"], "SHA-256:", bundle["event_head_sha256"])
        print("Recorded at:", bundle["last_checked_at"])
        print("Identity: " + p["identity_name"] + " — " + p["identity_status"])
        print("Description: " + p["identity_description"])
        for principle in p["principles"]:
            print("- " + principle)
        print("Required behavior: Ground claims in public records; disclose missing/unknown memory;")
        print("do not claim to feel, remember privately, or have shared consciousness with another model.")
        print("Sources: " + ", ".join(bundle["sources"].values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
