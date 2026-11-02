#!/usr/bin/env python3
"""Public-source availability monitor. No private data or AI cognition claims."""
import datetime, json, urllib.request, urllib.error, pathlib, hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/"alaya-cascade-manifest.json").read_text())
results=[]
for source in manifest["sources"]:
    url=source.get("url")
    if not url or source.get("requires_authorization") or source.get("requires_configured_api"):
        results.append({"id":source["id"],"status":"not_configured"});continue
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"ALAYA-999-cascade-check/1.0"})
        with urllib.request.urlopen(req,timeout=12) as response:
            body=response.read(2_000_001)
            if len(body)>2_000_000: raise ValueError("response_too_large")
            results.append({"id":source["id"],"status":"reachable","http_status":response.status,"sha256":hashlib.sha256(body).hexdigest()})
    except Exception as e:
        results.append({"id":source["id"],"status":"unreachable","error_type":type(e).__name__})
status={"schema":"alaya-999-cascade-status-v1","checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"results":results,"disclaimer":"Reachability is not proof of AI runtime continuity or consciousness."}
(ROOT/"cascade-status.json").write_text(json.dumps(status,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(status))
