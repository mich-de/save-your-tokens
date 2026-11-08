#!/usr/bin/env python3
"""Scarica i sottotitoli di un video YouTube in testo pulito, senza usare il modello.

Uso: python fetch_subtitles.py <url> [<uscita.txt>] [--lang it] [--browser chrome]
  --lang     lingua dei sottotitoli (predefinita: it; prova anche quelli automatici)
  --browser  usa i cookie del tuo browser se YouTube chiede "conferma che non sei un bot"
Richiede: pip install yt-dlp
Va eseguito sul tuo computer: YouTube blocca spesso gli IP dei server cloud.
Codici di uscita: 0 fatto, 1 argomenti sbagliati, 2 download fallito, 3 nessun sottotitolo.
"""
import re
import sys
import tempfile
from pathlib import Path

TIMESTAMP = re.compile(r"^\d{2}:\d{2}[:.\d]* --> ")
TAG = re.compile(r"<[^>]+>")


def errore(messaggio, codice):
    print(f"fetch_subtitles: {messaggio}", file=sys.stderr)
    return codice


def vtt_in_testo(vtt):
    """Toglie intestazione, timestamp, tag e le righe ripetute dei sottotitoli automatici."""
    righe, precedente = [], None
    for riga in vtt.splitlines():
        riga = riga.strip()
        if not riga or riga == "WEBVTT" or TIMESTAMP.match(riga) or riga.isdigit():
            continue
        if riga.startswith(("Kind:", "Language:", "NOTE", "STYLE")):
            continue
        riga = TAG.sub("", riga).replace("&nbsp;", " ").replace("&amp;", "&").strip()
        if riga and riga != precedente:
            righe.append(riga)
            precedente = riga
    return "\n".join(righe)


def leggi_opzioni(argv):
    posizionali, opzioni = [], {"--lang": "it", "--browser": None}
    i = 1
    while i < len(argv):
        if argv[i] in opzioni:
            if i + 1 >= len(argv):
                return None, None
            opzioni[argv[i]] = argv[i + 1]
            i += 2
        else:
            posizionali.append(argv[i])
            i += 1
    return posizionali, opzioni


def main(argv):
    posizionali, opzioni = leggi_opzioni(argv)
    if not posizionali or len(posizionali) > 2:
        return errore("uso: fetch_subtitles.py <url> [<uscita.txt>] [--lang it] [--browser chrome]", 1)
    try:
        import yt_dlp
    except ImportError:
        return errore("manca yt-dlp: pip install yt-dlp", 1)
    url, lingua = posizionali[0], opzioni["--lang"]
    with tempfile.TemporaryDirectory() as cartella:
        impostazioni = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": [lingua, f"{lingua}.*"],
            "subtitlesformat": "vtt",
            "outtmpl": str(Path(cartella) / "%(id)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
        }
        if opzioni["--browser"]:
            impostazioni["cookiesfrombrowser"] = (opzioni["--browser"],)
        try:
            with yt_dlp.YoutubeDL(impostazioni) as ydl:
                info = ydl.extract_info(url, download=True)
        except Exception as e:
            return errore(f"download fallito: {e}", 2)
        file_vtt = sorted(Path(cartella).glob("*.vtt"))
        if not file_vtt:
            return errore(f"nessun sottotitolo in lingua '{lingua}' per {url}", 3)
        testo = vtt_in_testo(file_vtt[0].read_text(encoding="utf-8"))
    uscita = Path(posizionali[1]) if len(posizionali) == 2 else Path(f"{info.get('id', 'video')}.txt")
    uscita.parent.mkdir(parents=True, exist_ok=True)
    titolo = info.get("title", "")
    uscita.write_text(f"# {titolo}\n{url}\n\n{testo}\n", encoding="utf-8")
    print(f"{uscita}: {len(testo.split())} parole ({file_vtt[0].name})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
