#!/usr/bin/env python3
"""Mostra la timeline dei token di una sessione Claude Code, senza usare il modello.

Legge il transcript JSONL della sessione e stampa, per ogni tuo messaggio, quante
richieste ha generato, quali tool ha usato e quanti token ha consumato. In fondo
elenca le richieste piu' costose: li' di solito c'e' lo spreco.

Uso: python session_timeline.py [<sessione.jsonl> | <cartella progetto>] [--top 5]
  senza argomenti: la sessione piu' recente in ~/.claude/projects/
  cartella:        la sessione piu' recente in quella cartella
Requisiti: solo libreria standard.
Codici di uscita: 0 fatto, 1 argomenti o file sbagliati, 2 nessuna richiesta nel file.

Colonne: nuovi = input + scrittura cache (token pagati pieni o quasi),
cache = letti dalla cache (costano circa un decimo), out = output.
"""
import json
import sys
from pathlib import Path


def errore(messaggio, codice):
    print(f"session_timeline: {messaggio}", file=sys.stderr)
    return codice


def trova_sessione(percorso):
    if percorso and percorso.is_file():
        return percorso
    base = percorso or Path.home() / ".claude" / "projects"
    if not base.is_dir():
        return None
    file = sorted(base.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    file = [f for f in file if "subagents" not in f.parts]
    return file[-1] if file else None


def testo_utente(contenuto):
    """Il testo scritto dall'utente, oppure None se il messaggio e' solo un risultato di tool."""
    if isinstance(contenuto, str):
        return contenuto
    parti = [c.get("text", "") for c in contenuto if isinstance(c, dict) and c.get("type") == "text"]
    return " ".join(parti) if parti else None


def leggi_turni(file):
    turni, richieste = [], {}
    for riga in file.open(encoding="utf-8"):
        try:
            d = json.loads(riga)
        except json.JSONDecodeError:
            continue
        if d.get("isSidechain"):
            continue
        m = d.get("message") or {}
        if d.get("type") == "user":
            testo = testo_utente(m.get("content", ""))
            if testo and not testo.lstrip().startswith("<"):
                turni.append({"testo": " ".join(testo.split()), "ora": d.get("timestamp", ""), "id": []})
        elif d.get("type") == "assistant" and m.get("usage"):
            rid = d.get("requestId") or d.get("uuid")
            r = richieste.setdefault(rid, {"tool": [], "modello": m.get("model", "?")})
            r["usage"] = m["usage"]  # le righe con lo stesso requestId ripetono l'usage: tengo l'ultima
            r["tool"] += [c.get("name", "?") for c in m.get("content", []) if c.get("type") == "tool_use"]
            if not turni:
                turni.append({"testo": "(inizio sessione)", "ora": d.get("timestamp", ""), "id": []})
            if rid not in turni[-1]["id"]:
                turni[-1]["id"].append(rid)
    return turni, richieste


def conta(u):
    nuovi = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
    return nuovi, u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0)


def k(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def main(argv):
    argomenti, top = [], 5
    i = 1
    while i < len(argv):
        if argv[i] == "--top" and i + 1 < len(argv) and argv[i + 1].isdigit():
            top, i = int(argv[i + 1]), i + 2
        else:
            argomenti.append(argv[i])
            i += 1
    if len(argomenti) > 1:
        return errore("uso: session_timeline.py [<sessione.jsonl> | <cartella>] [--top 5]", 1)
    file = trova_sessione(Path(argomenti[0]).expanduser() if argomenti else None)
    if not file:
        return errore("nessuna sessione .jsonl trovata", 1)
    turni, richieste = leggi_turni(file)
    if not richieste:
        return errore(f"nessuna richiesta con usage in {file}", 2)

    print(f"{file}\n")
    print(f"{'#':>3} {'ora':5} {'rich':>4} {'nuovi':>7} {'cache':>7} {'out':>6}  messaggio / tool")
    totale = [0, 0, 0]
    for n, t in enumerate(turni, 1):
        somma, tool = [0, 0, 0], []
        for rid in t["id"]:
            somma = [a + b for a, b in zip(somma, conta(richieste[rid]["usage"]))]
            tool += richieste[rid]["tool"]
        totale = [a + b for a, b in zip(totale, somma)]
        ora = t["ora"][11:16]
        print(f"{n:>3} {ora:5} {len(t['id']):>4} {k(somma[0]):>7} {k(somma[1]):>7} {k(somma[2]):>6}  {t['testo'][:60]}")
        if tool:
            conteggio = {}
            for nome in tool:
                conteggio[nome] = conteggio.get(nome, 0) + 1
            print(f"{'':31}  tool: " + ", ".join(f"{nome}x{c}" if c > 1 else nome for nome, c in conteggio.items()))
    print(f"\ntotale: {len(richieste)} richieste, nuovi {k(totale[0])}, cache {k(totale[1])}, out {k(totale[2])}")

    def costo(rid):
        nuovi, _, out = conta(richieste[rid]["usage"])
        return nuovi + out

    turno_di = {rid: n for n, t in enumerate(turni, 1) for rid in t["id"]}
    print(f"\nrichieste piu' costose (nuovi + out):")
    for rid in sorted(richieste, key=costo, reverse=True)[:top]:
        r = richieste[rid]
        nuovi, _, out = conta(r["usage"])
        print(f"  turno {turno_di.get(rid, '?'):>3}  nuovi {k(nuovi):>7}  out {k(out):>6}  {r['modello']}  {', '.join(r['tool']) or '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
