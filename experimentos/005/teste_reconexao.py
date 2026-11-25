"""Deterministic same-machine disconnect/reconnect test, not a field experiment."""
from argparse import ArgumentParser
import hashlib, json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.request import build_opener, ProxyHandler
from urllib.error import URLError

p=ArgumentParser(description=__doc__)
p.add_argument("anchor",type=Path)
a=p.parse_args()
digest="40f24581de77c1135eb8a30c06825c0381c60ce6c12b1bfb2aede601bf4a7c0e"
data=a.anchor.read_bytes()
assert hashlib.sha256(data).hexdigest()==digest
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!="/anchor":
            self.send_error(404);return
        self.send_response(200);self.end_headers();self.wfile.write(data)
    def log_message(self,*args): pass
def start(port=0):
    h=HTTPServer(("127.0.0.1",port),Handler)
    th=threading.Thread(target=h.serve_forever,daemon=True)
    th.start()
    return h
def stop(h):h.shutdown();h.server_close()
def fetch(h):
    with build_opener(ProxyHandler({})).open(f"http://127.0.0.1:{h}/anchor",timeout=2) as q:
        b=q.read()
        if hashlib.sha256(b).hexdigest()!=digest:
            raise RuntimeError("Unexpected bytes")
        return {"http":q.status,"bytes":len(b),"sha256":digest}
h=start()
port=h.server_port
before=fetch(port)
stop(h)
try:
    fetch(port)
except URLError:
    offline=True
else:
    raise RuntimeError("Origin not disconnected")
h=start(port)
try:
    after=fetch(port)
finally:
    stop(h)
print(json.dumps({"mode":"local loopback, one machine","before":before,"refused_during_interruption":offline,"after":after},indent=2))
