#!/usr/bin/env python3
"""Elenca i modelli con costo $0 in input e in output dal registro models.dev (la fonte di OpenCode), senza usare il modello.

Uso: python list_free_models.py [<provider>]
Due gruppi: "gratis" ha "free" nell'id o nel nome; "costo 0 dichiarato" ha solo il prezzo a zero, che puo' voler dire
modello locale, a tua chiave o prezzo non pubblicato: va controllato. Router e voci generiche (auto, custom) sono esclusi.
Codici di uscita: 0 fatto, 2 registro non raggiungibile o non valido.
"""
import json
import sys
import urllib.request

REGISTRO = "https://models.dev/api.json"
GENERICI = {"auto", "custom", "router", "default"}


def errore(messaggio, codice):
    print(f"list_free_models: {messaggio}", file=sys.stderr)
    return codice


def scarica():
    req = urllib.request.Request(REGISTRO, headers={"User-Agent": "OpenCode-Free-Scanner"})
    with urllib.request.urlopen(req, timeout=20) as risposta:
        return json.loads(risposta.read().decode("utf-8"))


def e_gratis(modello):
    """Serve il prezzo esplicito: chi non ha il campo cost ha prezzo ignoto, non zero."""
    costo = modello.get("cost")
    return isinstance(costo, dict) and costo.get("input") == 0 and costo.get("output") == 0


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    solo = argv[1].lower() if len(argv) > 1 else None
    try:
        dati = scarica()
    except Exception as e:
        return errore(f"{REGISTRO} non disponibile: {e}", 2)
    if not isinstance(dati, dict):
        return errore(f"{REGISTRO}: formato inatteso", 2)
    gratis, dichiarati = [], []
    for prov_id, prov in dati.items():
        if solo and prov_id.lower() != solo:
            continue
        modelli = prov.get("models") if isinstance(prov, dict) else None
        for mod_id, modello in (modelli or {}).items():
            if not isinstance(modello, dict) or not e_gratis(modello):
                continue
            if mod_id.rsplit("/", 1)[-1].lower() in GENERICI:
                continue
            nome = str(modello.get("name") or "")
            riga = f"{prov_id}/{mod_id:<45} | {nome}"
            (gratis if "free" in f"{mod_id} {nome}".lower() else dichiarati).append(riga)
    for titolo, righe in (("gratis", gratis), ("costo 0 dichiarato (da controllare)", dichiarati)):
        print(f"=== {titolo}: {len(righe)} ===")
        print("\n".join(sorted(righe)) if righe else "(nessuno)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
