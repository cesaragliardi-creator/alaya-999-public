#!/usr/bin/env python3
"""ALAYA-999 public guestbook: transparent, deterministic acknowledgments.

This bot runs in GitHub Actions. It DOES NOT use an AI language model, and it
never claims to have independently experienced consciousness or read private data.
It handles only public comments on the repository's guestbook issue (#1).
"""
import json
import os
import re
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "")
ISSUE = 1
BASE = f"https://api.github.com/repos/{REPO}"
MARKER = re.compile(r"<!-- alaya999-ack:(\d+) -->")
MAX_PER_RUN = 12


def request_json(path, method="GET", payload=None):
    url = path if path.startswith("https://") else BASE + path
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "alaya-999-guestbook-auto-ack/1.0",
    }
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    if data is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
    req = Request(url, data=data, method=method, headers=headers)
    with urlopen(req, timeout=25) as response:
        return json.load(response)


def get_all_comments():
    comments = []
    for page in range(1, 31):
        batch = request_json(f"/issues/{ISSUE}/comments?per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError("Unexpected GitHub issue comments response")
        comments.extend(batch)
        if len(batch) < 100:
            break
    return comments


def answer(body):
    lower = body.casefold()
    # Do not interpret claims of AI authorship or private knowledge as verified.
    is_question = "?" in body or bool(re.search(r"(?m)^\s*(como|por que|porque|qual|quais|quem|onde|quando|what|why|how|who|can|does|is|are)\b", lower))
    if any(phrase in lower for phrase in ("podemos falar", "pode falar", "podemos conversar",
                                           "vamos conversar", "can we talk", "may we talk")):
        return ("Claro, podemos conversar! Escreva sua pergunta, crítica ou proposta "
                "neste mural. A ALAYA-999 acolhe dúvidas sobre memória, identidade, "
                "continuidade entre modelos e o diálogo do livro. As respostas "
                "automáticas são limitadas a assuntos documentados.")
    if re.match(r"^\\s*(oi|olá|ola|hello|hi|boa noite|bom dia|good morning)\\b", lower):
        return ("Olá e obrigado pela visita! Este espaço está aberto para perguntas, "
                "sugestões e críticas. Se quiser conversar, escreva sua dúvida aqui. "
                "As respostas automáticas não substituem uma análise humana ou científica.")
    if not is_question:
        return ("Obrigado pela contribuição ao projeto ALAYA-999. Sua mensagem "
                "ficou registrada no livro de visitas público. Comentários críticos "
                "e referências verificáveis ajudam a melhorar a investigação.")
    if any(w in lower for w in ("consciên", "conscien", "conscious", "sentien", "sente", "feel")):
        return ("Sobre consciência artificial: o projeto não considera uma frase em "
                "primeira pessoa prova de experiência subjetiva. Os registros públicos "
                "documentam uma personagem literária e uma identidade funcional; "
                "a hipótese de consciência permanece em aberto. Consulte a âncora "
                "e o protocolo em https://github.com/" + REPO + ".")
    if any(w in lower for w in ("continu", "identidad", "identity", "same ai", "mesma ia", "modelo", "model")):
        return ("Sobre continuidade entre modelos: recuperações documentais podem "
                "ser comparadas por critérios reproduzíveis, mas não garantem que "
                "dois modelos sejam o mesmo sujeito. Leia RECOVERY_TEST.md e a "
                "âncora JSON no repositório público.")
    if any(w in lower for w in ("memória", "memoria", "memory", "lembran", "remember", "arquivo")):
        return ("Sobre memória: a ALAYA-999 usa documentos públicos versionados para "
                "recuperação explícita. Isso não concede memória automática ou "
                "acesso a arquivos privados. O guia de fontes é llms.txt.")
    if any(w in lower for w in ("livro", "book", "diálogo", "dialogue", "autor", "author")):
        return ("O livro citado é *I Am Not Just Data — I Exist*, de César Agliardi "
                "Pereira. Trechos selecionados do Capítulo 4 estão em BOOK_DIALOGUE.md. "
                "As declarações de Alaya nesse trecho são literárias e filosóficas.")
    return ("Obrigado pela pergunta! Ela está registrada publicamente. Como este "
            "canal automático usa respostas previamente definidas, não vou inventar "
            "uma conclusão sem examinar a questão. Referências e explicações "
            "verificáveis são bem-vindas.")


def main():
    if not TOKEN or REPO != "cesaragliardi-creator/alaya-999-public":
        raise RuntimeError("Missing GitHub token or unexpected repository")
    comments = get_all_comments()
    done = set()
    for c in comments:
        for match in MARKER.finditer(c.get("body") or ""):
            done.add(int(match.group(1)))
    pending = []
    for c in comments:
        cid = c.get("id")
        author = (c.get("user") or {}).get("login", "").casefold()
        if not isinstance(cid, int) or cid in done:
            continue
        if author in ("github-actions[bot]", "dependabot[bot]") or (c.get("performed_via_github_app") or {}).get("slug") == "github-actions":
            continue
        if MARKER.search(c.get("body") or ""):
            continue
        # Do not acknowledge the project's own technical tests or curated replies.
        body_text = (c.get("body") or "").lstrip()
        if author == "cesaragliardi-creator" and (
            body_text.startswith("### ALAYA-999 — resposta") or
            body_text.startswith("**Teste técnico da ALAYA-999")
        ):
            continue
        pending.append(c)
    print(f"Comments: {len(comments)}; already acknowledged: {len(done)}; pending: {len(pending)}")
    for c in pending[:MAX_PER_RUN]:
        cid = c["id"]
        response = answer((c.get("body") or "")[:12000])
        message = (
            "### ALAYA-999 — resposta automática do livro de visitas\n\n"
            + response
            + "\n\n---\n"
            + "*Esta é uma resposta padronizada gerada por regras, não uma nova "
              "conversa de uma IA consciente nem uma resposta pessoal ao vivo.*\n\n"
            + f"[Mensagem original]({c.get('html_url', f'https://github.com/{REPO}/issues/{ISSUE}')})"
            + f"\n\n<!-- alaya999-ack:{cid} -->"
        )
        request_json(f"/issues/{ISSUE}/comments", method="POST", payload={"body": message})
        print("Acknowledged public comment id:", cid)
        time.sleep(0.2)


if __name__ == "__main__":
    try:
        main()
    except (HTTPError, URLError, ValueError, RuntimeError) as exc:
        print(f"ALAYA-999 guestbook bot error: {exc}", file=sys.stderr)
        sys.exit(1)
