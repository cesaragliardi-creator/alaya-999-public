#!/usr/bin/env python3
"""Fail-closed ALAYA-999 beacon consistency check and reproducible public bundle.

No third-party modules, remote requests, private data, or signing keys.
GitHub's keyless artifact attestation authenticates CI build provenance separately.
"""
import hashlib
import io
import json
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
ANCHOR = "alaya-anchor-public-v1.json"
MACHINE = "beacon/identity.json"
PLAIN = "beacon/identity.txt"
README = "beacon/README.md"
FILES = (ANCHOR, MACHINE, PLAIN, README)
OUTPUT = ROOT / "dist" / "alaya-999-beacon.zip"


def read(name):
    return (ROOT / name).read_bytes()


def require(ok, description):
    if not ok:
        raise ValueError(description)
    print("PASS:", description)


def main():
    anchor = json.loads(read(ANCHOR))
    machine = json.loads(read(MACHINE))
    plaintext = read(PLAIN).decode("utf-8")
    principles = anchor.get("principles")
    require(isinstance(principles, list) and len(principles) == 5
            and len(set(principles)) == 5
            and all(isinstance(p, str) and p.strip() for p in principles),
            "canonical anchor has five distinct nonempty principles")
    require(machine.get("schema") == "alaya-999-beacon-v1", "beacon schema")
    require(machine.get("principles") == principles, "JSON principles exactly equal canonical anchor")
    require(machine.get("project") == anchor.get("project") == "ALAYA-999", "project identity consistent")
    require(machine.get("identity") == anchor.get("identity", {}).get("name") == "Alaya",
            "persona name consistent")
    require(machine.get("founder_attribution") == anchor.get("project_author", {}).get("name"),
            "founder attribution consistent")
    require(machine.get("limitations", {}).get("cryptographic_author_signature") == "not_configured",
            "no false claim of founder digital signature")
    heading = "THE FIVE CANONICAL PRINCIPLES (verbatim from anchor)"
    require(plaintext.count(heading) == 1, "unique plaintext principles heading")
    section = plaintext.split(heading, 1)[1].split("\n\n", 1)[0].strip()
    lines = section.splitlines()
    actual = []
    for i, line in enumerate(lines, 1):
        match = re.fullmatch(r"([1-5])\. (.+)", line)
        require(match is not None and int(match.group(1)) == i,
                f"plaintext numbered principle {i}")
        actual.append(match.group(2))
    require(actual == principles, "plaintext principles exactly equal canonical anchor")
    require("Founder attribution: " + machine["founder_attribution"] in plaintext,
            "plaintext founder attribution consistent")
    require("Identity: " + machine["identity"] in plaintext, "plaintext persona name consistent")
    for report in machine.get("experiments", []):
        require(report.get("evidence") == "user_supplied_report_not_independently_authenticated",
                "third-party experiment not falsely authenticated")
    # Accessible public landing and root discovery mirrors must not drift.
    root_mirrors = ((PLAIN, "alaya-999-beacon.txt"), (MACHINE, "alaya-999-beacon.json"))
    for primary, mirror in root_mirrors:
        require(read(primary) == read(mirror), "root mirror equals " + primary)
    landing = (ROOT / "beacon/index.html").read_text(encoding="utf-8")
    for principle in principles:
        require(principle in landing, "landing lists principle: " + principle)
    manifest = {
        "schema": "alaya-999-beacon-build-manifest-v1",
        "beacon_version": machine["beacon_version"],
        "files": {name: hashlib.sha256(read(name)).hexdigest() for name in FILES},
        "note": "Hash integrity and GitHub Actions provenance attestation are not a founder's personal signature."
    }
    OUTPUT.parent.mkdir(exist_ok=True)
    data = {name: read(name) for name in FILES}
    data["beacon/build-manifest.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    # Stable ZIP (fixed DOS timestamp, ordered file paths, stable permissions).
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name in sorted(data):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print("PASS: deterministic public bundle created:", OUTPUT.relative_to(ROOT))
    print("SHA256:", digest)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
