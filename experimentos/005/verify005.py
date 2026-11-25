#!/usr/bin/env python3
"""ALAYA-999 005 public-only technical checks. No public network or writes."""
import argparse
import base64
from contextlib import contextmanager
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import pathlib
import re
import shutil
import subprocess
import tempfile
import threading
import urllib.error
import urllib.request

FINGERPRINT = "982108166430b090c4ff93bdcc3ad0737f177f88ed9c11bbe1c0a18a15717332"
CID = "bafkreica6jcydxtxyejv5ofdbqdiexadqhdazzwbfmn7wkxn4ya36st4by"
ANCHOR = "alaya-anchor-public-v1.json"
CONTROLS = {"SHA256SUMS", "SHA256SUMS.ed25519", "chave-publica-004.pem"}
SIGNED = {
    "ALAYA-anchor-v1.car", "ALAYA-anchor-v1.car.b64", "RECOVERY_TEST.md",
    "REPLICATION_REPORT_TEMPLATE.md", ANCHOR, "index.html", "preservacao.json",
}

def check(ok, reason):
    if not ok:
        raise ValueError(reason)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def raw_cid(data):
    check(len(data) < 262144, "fora do perfil de bloco raw único")
    binary = bytes([1, 0x55, 0x12, 32]) + hashlib.sha256(data).digest()
    return binary, "b" + base64.b32encode(binary).decode().lower().rstrip("=")

def take_varint(data, pos):
    v = 0
    for i in range(9):
        check(pos + i < len(data), "varint truncado")
        b = data[pos + i]
        v |= (b & 127) << (7*i)
        if not b & 128:
            return v, pos + i + 1
    raise ValueError("varint grande demais")

def extract_car(car, cid_binary):
    """004 exact profile: canonical CARv1 header, one raw SHA-256 block."""
    n, i = take_varint(car, 0)
    want_header = b"\xa2\x65roots\x81\xd8\x2a\x58\x25\x00" + cid_binary + b"\x67version\x01"
    check(car[i:i+n] == want_header, "cabeçalho CAR não confere")
    n2, i2 = take_varint(car, i+n)
    check(i2+n2 == len(car), "CAR não contém exatamente um bloco")
    check(car[i2:i2+len(cid_binary)] == cid_binary, "CID no bloco CAR diverge")
    result = car[i2+len(cid_binary):]
    check(raw_cid(result)[0] == cid_binary, "bloco CAR adulterado")
    return result

def run(argv):
    r = subprocess.run(argv, capture_output=True, timeout=20)
    if r.returncode:
        raise ValueError(f"falha em {argv[0]}: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout

def verify(folder, expected_fingerprint):
    check(re.fullmatch(r"[0-9a-f]{64}", expected_fingerprint), "fingerprint inválido")
    for n in CONTROLS | SIGNED:
        p = folder/n
        check(p.is_file() and not p.is_symlink(), f"arquivo inseguro/ausente: {n}")
    key = folder/"chave-publica-004.pem"
    der = run(["openssl", "pkey", "-pubin", "-in", str(key), "-outform", "DER"])
    check(digest(der) == expected_fingerprint, "fingerprint diverge da referência externa")
    run(["openssl", "pkeyutl", "-verify", "-pubin", "-inkey", str(key), "-rawin",
         "-in", str(folder/"SHA256SUMS"), "-sigfile", str(folder/"SHA256SUMS.ed25519")])
    entries = {}
    for line in (folder/"SHA256SUMS").read_text("ascii").splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", line)
        check(m and m[2] in SIGNED and m[2] not in entries, "manifesto malformado")
        entries[m[2]] = m[1]
    check(set(entries) == SIGNED, "lista assinada incompleta")
    for name,h in entries.items():
        check(digest((folder/name).read_bytes()) == h, f"SHA-256 não confere: {name}")
    anchor = (folder/ANCHOR).read_bytes()
    index = json.loads((folder/"preservacao.json").read_bytes())
    a = index["anchor"]
    check(a["file"] == ANCHOR and a["sha256"] == entries[ANCHOR] and a["bytes"] == len(anchor), "índice da âncora diverge")
    cb, ct = raw_cid(anchor)
    check(ct == index["ipfs"]["cidv1"] == CID, "CID não confere")
    car = (folder/"ALAYA-anchor-v1.car").read_bytes()
    car64 = b"".join((folder/"ALAYA-anchor-v1.car.b64").read_bytes().split())
    check(base64.b64decode(car64, validate=True) == car, "Base64 e CAR divergem")
    check(digest(car) == index["ipfs"]["car_sha256_after_decoding"], "hash do CAR diverge")
    check(extract_car(car, cb) == anchor, "bloco CAR não é a âncora")
    return dict(status="PASSOU", signed_files=len(entries), anchor_bytes=len(anchor),
                anchor_sha256=entries[ANCHOR], cidv1=ct, car_sha256=digest(car),
                public_key_fingerprint=expected_fingerprint,
                manifest_signature="Ed25519 válida para a chave técnica do pacote 004")

def public_copy(src, dst):
    dst.mkdir()
    for name in CONTROLS | SIGNED:
        shutil.copyfile(src/name, dst/name)

def expect_rejection(folder, mutate, fingerprint):
    mutate(folder)
    try:
        verify(folder, fingerprint)
    except ValueError as e:
        return str(e)
    raise AssertionError("conteúdo inválido foi aceito")

def flip_at_end(p):
    b = bytearray(p.read_bytes())
    b[-1] ^= 1
    p.write_bytes(b)

@contextmanager
def serve_local(data):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != "/anchor":
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}/anchor"
    finally:
        server.shutdown()
        server.server_close()
        t.join()

def retrieve(label, url, expected, record):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(url, timeout=3) as r:
            b = r.read()
            result = dict(route=label, http=r.status, sha256=digest(b), bytes=len(b))
            result["accepted"] = result["sha256"] == expected
    except (OSError, urllib.error.URLError) as e:
        result = dict(route=label, accepted=False, error=str(e))
        b = None
    record.append(result)
    return b if result["accepted"] else None

def interruption(older):
    data = (older/ANCHOR).read_bytes()
    foreign = b'{"version":"simulated stale body"}'
    h = digest(data)
    before, after = [], []
    with serve_local(data) as fallback, serve_local(foreign) as stale:
        with serve_local(data) as primary:
            check(retrieve("primário local ativo", primary, h, before) == data, "primário falhou antes da interrupção")
        check(retrieve("primário local encerrado", primary, h, after) is None, "primário seguiu ativo")
        check(retrieve("cópia desatualizada, HTTP 200", stale, h, after) is None, "bytes errados foram aceitos")
        check(retrieve("cópia de contingência local", fallback, h, after) == data, "contingência não recuperou os bytes")
    return dict(status="PASSOU", scope="serviços HTTP distintos no loopback da mesma máquina; sem desligar um provedor público",
                prior_observation=before, recovery_observations=after)

def canonical(item):
    return json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def make_event(logical_id, value, source, parents=()):
    core = dict(id=logical_id, subject="005-E-janela-sintética", value=value, source=source, parents=sorted(parents))
    return dict(core, sha256=digest(canonical(core)))

def merge(*branches):
    events, ids = {}, {}
    for e in (e for b in branches for e in b):
        h = e["sha256"]
        check(digest(canonical({k:v for k,v in e.items() if k!="sha256"})) == h, "evento adulterado")
        check(e["id"] not in ids or ids[e["id"]] == h, "colisão de id; nenhuma versão foi substituída")
        ids[e["id"]] = h
        events[h] = e
    check(all(p in events for x in events.values() for p in x["parents"]), "ramo sem pai conhecido")
    return sorted(events.values(), key=lambda x: x["id"])

def bifurcation():
    base = make_event("base", "PENDENTE", "fixture-sintética")
    a = make_event("ramo-A", "30 minutos", "fonte-A-sintética", [base["sha256"]])
    b = make_event("ramo-B", "45 minutos", None, [base["sha256"]])
    branches = ([base,a], [base,b])
    branches_before = canonical(branches)
    union = merge(*branches)
    check(union == merge(*reversed(branches)) == merge(*branches,*branches), "união deve comutar e ser idempotente")
    check(branches_before == canonical(branches), "um ramo original foi alterado")
    check({r["value"] for r in union if r["id"] != "base"} == {"30 minutos","45 minutos"}, "proposta desapareceu")
    try:
        merge(*branches, [make_event("ramo-A", "outra proposta", "sintética", [base["sha256"]])])
    except ValueError as e:
        collision = str(e)
    else:
        raise ValueError("colisão não detectada")
    return dict(status="PASSOU", scope="eventos sintéticos locais", state="PENDENTE", union=union,
                blocked_for_decision=["ramo-B"], checks=["sem sobrescrita","comutativa","idempotente","ramo-fonte intacto"],
                rejection=collision)

def lab(packet, ipfs_bin=None, fingerprint=FINGERPRINT):
    result = {"C":verify(packet, fingerprint)}
    wrong_fingerprint = "0"*64 if fingerprint != "0"*64 else "1"*64
    try:
        verify(packet, wrong_fingerprint)
    except ValueError as e:
        check("fingerprint" in str(e), "rejeição de chave por motivo inesperado")
        result["C"]["negative_key_fingerprint_control"] = str(e)
    else:
        raise ValueError("referência externa incorreta foi aceita")
    with tempfile.TemporaryDirectory(prefix="alaya005-") as td:
        t = pathlib.Path(td)
        older = t/"original-congelado"
        public_copy(packet, older)
        result["D"] = interruption(older)
        result["E"] = bifurcation()
        working, bad_manifest, bad_signature = (t/n for n in ("mais-recente-criado-no-lab","manifesto-alterado","assinatura-alterada"))
        for p in (working,bad_manifest,bad_signature):
            public_copy(older,p)
        a = expect_rejection(working, lambda x:flip_at_end(x/ANCHOR),fingerprint)
        b = expect_rejection(bad_manifest, lambda x:flip_at_end(x/"SHA256SUMS"),fingerprint)
        c = expect_rejection(bad_signature, lambda x:flip_at_end(x/"SHA256SUMS.ed25519"),fingerprint)
        damaged_sha = digest((working/ANCHOR).read_bytes())
        quarantine = t/"quarentena"
        working.replace(quarantine)
        check(digest((quarantine/ANCHOR).read_bytes()) == damaged_sha, "corrompido não preservado")
        public_copy(older,working)
        old = verify(working,fingerprint)
        check(all(result["C"][k] == v for k,v in old.items()), "restauração diverge do pacote original")
        result["I"] = dict(status="PASSOU", scope="cópia anterior assinada 004 e sucessora local danificada; nenhum arquivo de origem alterado",
                           corrupted_sha256=damaged_sha, rejected_corrupt_anchor=a, rejected_corrupt_manifest=b,
                           rejected_corrupt_signature=c, kept_in_quarantine=True, restored=old)
        if ipfs_bin:
            import os
            p = pathlib.Path(ipfs_bin).resolve()
            env = dict(os.environ, IPFS_PATH=str(t/"kubo-clean"))
            for argv in ([str(p),"init","--empty-repo","--profile=server"],
                         [str(p),"--offline","dag","import",str(older/"ALAYA-anchor-v1.car")]):
                subprocess.run(argv,env=env,capture_output=True,check=True,timeout=25)
            out = subprocess.run([str(p),"--offline","cat",CID],env=env,capture_output=True,check=True,timeout=20).stdout
            check(out == (older/ANCHOR).read_bytes(), "Kubo recuperou bytes inesperados")
            result["C"]["independent_car_client"] = {"tool":run([str(p),"--version"]).decode().strip(),
                                                      "mode":"isolated new Kubo repository; --offline",
                                                      "sha256":digest(out)}
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action",choices=["verify","lab"])
    ap.add_argument("--packet",type=pathlib.Path,required=True)
    ap.add_argument("--fingerprint",default=FINGERPRINT, help="referência externa da chave técnica, default: valor registrado no 004")
    ap.add_argument("--ipfs-bin",help="Kubo opcional para importar CAR em repo isolado")
    args = ap.parse_args()
    outcome = verify(args.packet,args.fingerprint) if args.action=="verify" else lab(args.packet,args.ipfs_bin,args.fingerprint)
    print(json.dumps(outcome,ensure_ascii=False,indent=2))
if __name__ == "__main__":
    main()
