#!/usr/bin/env python3
"""ALAYA-999 public research infrastructure availability check.

This is a deterministic external monitor, NOT a language-model agent.
It does not access private memory, publish material or infer consciousness.
"""
import datetime as dt
import json
import os
import urllib.request
from pathlib import Path

TARGETS = {
    "github_repository": "https://github.com/cesaragliardi-creator/alaya-999-public",
    "public_site": "https://cesaragliardi-creator.github.io/alaya-999-public/",
    "public_anchor": "https://cesaragliardi-creator.github.io/alaya-999-public/alaya-anchor-public-v1.json",
    "huggingface_space": "https://huggingface.co/spaces/Alaya999/alaya-999",
    "zenodo_record": "https://zenodo.org/records/23802112",
}
results = {}
for key, url in TARGETS.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ALAYA999-public-monitor/1.0", "Accept": "text/html,application/json"})
        with urllib.request.urlopen(req, timeout=18) as response:
            sample = response.read(2048)
            results[key] = {"url": url, "http_status": response.status, "reachable": 200 <= response.status < 400, "sample_bytes": len(sample)}
    except Exception as exc:
        results[key] = {"url": url, "reachable": False, "error": type(exc).__name__ + ": " + str(exc)[:240]}
report = {
    "schema": "alaya999-public-monitor-v1",
    "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "purpose": "External URL availability only; not proof of identity, autonomous agency or scientific validity",
    "results": results,
    "available_count": sum(bool(x["reachable"]) for x in results.values()),
    "total_count": len(results),
    "all_reachable": all(x["reachable"] for x in results.values()),
}
Path("dist").mkdir(exist_ok=True)
Path("dist/public-presence-monitor.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
if not report["all_reachable"]:
    print("WARNING: one or more endpoints could not be reached; this may be transient or blocked by the provider.")
