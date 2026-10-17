
# Laboratorul 5 - Lucrarea A
# Decoder universal: recunoaștere și decodificare

import argparse
import base64
import binascii
import hashlib
import json
import re
import urllib.parse
from pathlib import Path


# A1. Transformă textul în bytes și bytes în hex.
def text_la_bytes(s):
    return s.encode("utf-8")


def bytes_la_hex(b):
    return b.hex()


# A2. Identifică tipul de codificare.
def ghici_strat(s):
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"

    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"

    if (
        len(s) % 4 == 0
        and re.fullmatch(r"[A-Za-z0-9+/]*={0,2}", s)
    ):
        try:
            rezultat = base64.b64decode(s, validate=True)
            if base64.b64encode(rezultat).decode() == s:
                return "base64"
        except (ValueError, binascii.Error):
            pass

    return "necunoscut"


# A3. Decodifică un singur strat.
def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s, validate=True)
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "url":
        rezultat = urllib.parse.unquote(s).encode("utf-8")
    else:
        rezultat = s.encode("utf-8")

    return strat, rezultat


# A4. Încearcă să elimine mai multe straturi.
def decodifica_straturi(s):
    date = s.encode("utf-8")

    for _ in range(8):
        try:
            text = date.decode("utf-8")
        except UnicodeDecodeError:
            break

        strat = ghici_strat(text)

        if strat == "necunoscut":
            break

        _, rezultat = desfa(text)

        if rezultat == date:
            break

        date = rezultat

    return date


# A5. Încearcă toate cele 256 de chei XOR.
def sparge_xor(cale):
    date = Path(cale).read_bytes()
    rezultate = []

    for cheie in range(256):
        clar = bytes(octet ^ cheie for octet in date)

        if all(32 <= octet < 127 for octet in clar):
            rezultate.append((cheie, clar.decode("ascii")))

    return rezultate


# A6. Caută parolele din dicționar care corespund hashurilor.
def sparge_hashuri(cale_hashuri, cale_wordlist):
    hashuri = Path(cale_hashuri).read_text(
        encoding="utf-8"
    ).splitlines()

    cuvinte = Path(cale_wordlist).read_text(
        encoding="utf-8"
    ).splitlines()

    algoritmi = {
        32: "md5",
        40: "sha1",
        64: "sha256",
    }

    gasite = []

    for tinta in hashuri:
        tinta = tinta.strip().lower()

        if not tinta:
            continue

        algoritm = algoritmi.get(len(tinta))

        if algoritm is None:
            continue

        for cuvant in cuvinte:
            calculat = hashlib.new(
                algoritm, cuvant.encode("utf-8")
            ).hexdigest()

            if calculat == tinta:
                gasite.append((algoritm, cuvant))
                break

    return gasite


# A7. Interfața în linia de comandă.
def main():
    parser = argparse.ArgumentParser(
        description="Decoder universal"
    )

    parser.add_argument(
        "intrare",
        help="Șirul de decodat sau calea fișierului"
    )

    parser.add_argument(
        "--fisier",
        action="store_true",
        help="Citește intrarea dintr-un fișier"
    )

    args = parser.parse_args()

    if args.fisier:
        date = Path(args.intrare).read_bytes()
        strat = "fisier"
    else:
        strat = ghici_strat(args.intrare)
        date = decodifica_straturi(args.intrare)

    fisa = {
        "strat": strat,
        "rezultat": date.hex()
    }

    cale_fisa = Path(__file__).with_name("fisa.json")

    cale_fisa.write_text(
        json.dumps(fisa, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(fisa, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()

    