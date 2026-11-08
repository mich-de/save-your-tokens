#!/usr/bin/env python3
"""Hook deterministico che indirizza Claude allo step o allo script giusto, senza usare il modello.

Un solo file, tre eventi di Claude Code (il primo argomento dice quale):
  prompt   UserPromptSubmit: cerca nel messaggio i trigger della tabella e aggiunge al
           contesto UNA riga con lo step da leggere o lo script da lanciare. Niente match, niente output.
  pretool  PreToolUse su Read: nega la lettura nativa di un PDF (c'e' lo script), chiede conferma
           per le immagini (OCR prima, a meno che vadano viste).
  start    SessionStart: se HANDOFF.md e' stato modificato da meno di 2 ore, dice di riprendere da li'.

Uso: python token_router.py prompt|pretool|start   (legge il JSON dell'evento da stdin)
Variabili: SYT_DIR = cartella di save-your-tokens (predefinita: la cartella sopra scripts/hooks)
           SYT_HANDOFF_HOURS = finestra per HANDOFF.md (predefinita: 2)
Requisiti: solo libreria standard. Esce sempre 0: un hook rotto non deve bloccare la sessione.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

QUI = Path(__file__).resolve().parent
REPO = Path(os.environ.get("SYT_DIR", QUI.parent.parent))

# (regex sul prompt, puntatore). Ordine = priorita'. Al massimo due puntatori per messaggio.
TRIGGER = [
    (r"youtu\.?be", "video: run scripts/fetch_subtitles.py on your machine, paste the text (step 07)"),
    (r"\S+\.pdf\b", "PDF: run scripts/extract_pdf.py, do not Read it natively (step 07)"),
    (r"\S+\.(png|jpe?g|webp)\b", "image: OCR with scripts/extract_image_ocr.py if it is text; Read it only if it must be seen (step 07)"),
    (r"\b(ui|ux|front-?end|landing|dashboard|layout|pagin[ae]|page|componente?|css|tailwind|react|mockup|wireframe|design)\b",
     "UI work: ASCII wireframe first (step 05), then step 17 rules"),
    (r"\b(subagent|sub-agent|agenti?|agents?|parallel[oi]?|team|workflow)\b", "subagents: step 11 (default Haiku, effort by task)"),
    (r"(/model|\bmodell[oi]\b|\bmodels?\b|\bopus\b|\bsonnet\b|\bhaiku\b|\bfable\b|\beffort\b)",
     "model choice: step 02; never switch mid-task, it rebuilds the cache (step 20)"),
    (r"\b(mcp|connettor\w*|connectors?|plugins?|server)\b", "MCP/connectors: prefer a CLI (step 08), prune idle ones (step 06)"),
    (r"\b(hooks?)\b", "hooks: step 07 (reviewed hooks, install scope)"),
    (r"(/compact|/clear|\bcompatt\w*|\bcompact\w*|\bhandoff\b|\bcheckpoint\b|\briprend\w*|\bresume\b|\bcontext\b|\bcontesto\b)",
     "session state: HANDOFF.md + /clear (steps 03-04); compact only on a warm cache (step 21)"),
    (r"\b(tokens?|cost[oi]?|costs?|usage|quota|credit[is]?|crediti|spes[ao]|spend\w*|burn)\b",
     "cost: scripts/session_timeline.py shows where tokens went (step 24); audit with step 22"),
    (r"\b(proxy|network|rete|curl|blocked|bloccat[oa]|firewall|vpn|tether\w*|android)\b", "network: step 13 (proxy, curl.exe checks); phone as proxy: step 16"),
    (r"\b(opencode|free models?|gratis|gratuit[oi]|\$0|rate.?limit\w*|429)\b", "free models and quotas: steps 14-15 (scripts/list_free_models.py)"),
    (r"\b(status ?line|statusline|barra di stato)\b", "status line: step 18 (scripts/statusline.py)"),
    (r"\b(doctor|prompt-audit|skill-doctor|skills?|memory|memoria|claude\.md|agents\.md)\b",
     "instruction files and skills: steps 06 and 23 (/doctor prompt-audit, /skill-doctor)"),
    (r"\b(graph|grafo|codebase|repo grande|large repo|monorepo)\b", "large codebase navigation: step 09"),
    (r"\b(script|automat\w*|deterministic\w*|ripetitiv\w*|repeatable)\b", "repeatable step: make it code, not a prompt (step 10)"),
]
MAX_PUNTATORI = 2
IMMAGINI = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp")


def leggi_evento():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def rispondi(evento, **campi):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": evento, **campi}}))


def prompt(evento):
    testo = (evento.get("prompt") or "").lower()
    if len(testo) < 4 or testo.startswith("/"):  # comandi slash e messaggi vuoti: niente da indirizzare
        return
    puntatori = []
    for regex, puntatore in TRIGGER:
        if re.search(regex, testo) and puntatore not in puntatori:
            puntatori.append(puntatore)
            if len(puntatori) == MAX_PUNTATORI:
                break
    if puntatori:
        rispondi("UserPromptSubmit", additionalContext="save-your-tokens -> " + "; ".join(puntatori) + ". Read only that step.")


def pretool(evento):
    if evento.get("tool_name") != "Read":
        return
    percorso = str((evento.get("tool_input") or {}).get("file_path", "")).lower()
    if percorso.endswith(".pdf"):
        rispondi("PreToolUse", permissionDecision="deny",
                 permissionDecisionReason="Native PDF read costs 1,500-3,000 tokens/page. Run: python scripts/extract_pdf.py <file.pdf> out.txt, then Read out.txt (step 07).")
    elif percorso.endswith(IMMAGINI):
        rispondi("PreToolUse", permissionDecision="ask",
                 permissionDecisionReason="Text screenshot? OCR it first: python scripts/extract_image_ocr.py <img> out.txt (step 07). Allow only if the image must be seen (chart, mockup, diagram).")


def start(evento):
    if evento.get("source") == "compact":
        return
    radice = Path(evento.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ".")
    handoff = radice / "HANDOFF.md"
    if not handoff.is_file():
        return
    ore = float(os.environ.get("SYT_HANDOFF_HOURS", "2"))
    minuti = (time.time() - handoff.stat().st_mtime) / 60
    if minuti <= ore * 60:
        rispondi("SessionStart", additionalContext=f"HANDOFF.md was updated {int(minuti)} min ago: read it and resume from its 'Next step' section (step 04). Do not re-explore what it already records.")


def main(argv):
    azioni = {"prompt": prompt, "pretool": pretool, "start": start}
    if len(argv) != 2 or argv[1] not in azioni:
        print("token_router: uso: token_router.py prompt|pretool|start", file=sys.stderr)
        return 0
    try:
        azioni[argv[1]](leggi_evento())
    except Exception as e:  # mai bloccare la sessione per un hook
        print(f"token_router: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
