#!/usr/bin/env python3
"""Read ALAYA-999 public profile snapshots from a verified durable event chain.

A separate process can use this command without the original source documents.
Only explicit historical snapshots are returned; missing evidence stays missing.
"""
import argparse
import json
from pathlib import Path

from autonomous_public_memory import InvalidMemory, read_state, recover_profile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root", type=Path, required=True)
    parser.add_argument("--at-sequence", type=int)
    args = parser.parse_args()
    try:
        events, current = read_state(args.state_root)
        if current is None:
            raise InvalidMemory("no previously recorded public memory")
        result = recover_profile(events, args.at_sequence)
        result["archive_events"] = len(events)
        result["archive_head_sha256"] = current["head_hash"]
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    except (ValueError, OSError) as exc:
        parser.exit(2, "ALAYA999_PUBLIC_RECALL_FAILED: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
