
# Laboratorul 5 - Lucrarea A
# Decoder universal: recunoaștere și decodificare

import base64
import binascii
import urllib.parse
import re


# A2. Recunoaștem stratul după formă

def ghici_strat(s):
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"

    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"

    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"

    return "necunoscut"


# A3. Desfacem stratul recunoscut
def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s)
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "url":
        rezultat = urllib.parse.unquote(s).encode()
    else:
        rezultat = s.encode()

    return strat, rezultat

# A4. Verificăm dacă octeții formează text citibil
def citibil(b):
    return all(32 <= c < 127 for c in b)
#  Decodificăm mesajul pe mai multe straturi
def decodifica_straturi(s):
    b = s.encode()

    for _ in range(8):
        try:
            text = b.decode("utf-8")
        except UnicodeDecodeError:
            break

        # Dacă este Hex, decodificăm stratul
        if re.fullmatch(r"[0-9a-fA-F]+", text) and len(text) % 2 == 0:
            b = bytes.fromhex(text)
            break

        # Dacă este URL, decodificăm stratul
        if re.search(r"%[0-9a-fA-F]{2}", text):
            b = urllib.parse.unquote(text).encode()
            continue

        # Dacă nu mai avem un strat recunoscut, ne oprim
        try:
            rezultat = base64.b64decode(text, validate=True)
            if base64.b64encode(rezultat).decode() == text:
                b = rezultat
                # Continuăm dacă rezultatul este Hex sau URL
                try:
                    urmator = b.decode("utf-8")
                except UnicodeDecodeError:
                    break

                if (
                    re.fullmatch(r"[0-9a-fA-F]+", urmator)
                    and len(urmator) % 2 == 0
                ) or re.search(r"%[0-9a-fA-F]{2}", urmator):
                    continue
                break
        except (ValueError, binascii.Error):
            pass

        break

    return b



# A1. Text și octeți: încălzirea

s = "Salut"

b = s.encode()

print(b, b[0])

# Transformăm octeții în reprezentare Hex
print(b.hex())

# Refacem octeții din reprezentarea Hex
b_refacut = bytes.fromhex(b.hex())
print(b_refacut)


def decode_hex(text):
    try:
        rezultat = bytes.fromhex(text).decode("utf-8")
        return rezultat
    except (ValueError, UnicodeDecodeError):
        return None


print(decode_hex("53414c5554"))
print(decode_hex("4d6f6c646f7661"))



def decode_base64(text):
    try:
        rezultat = base64.b64decode(text, validate=True).decode("utf-8")
        return rezultat
    except (ValueError, UnicodeDecodeError, binascii.Error):
        return None

print(decode_base64("U0FMVVQ="))



def decode_url(text):
    rezultat = urllib.parse.unquote(text)
    if rezultat != text:
        return rezultat
    return None

print(decode_url("Salut%20Moldova"))


def decode_xor(data, key):
    rezultat = bytes(b ^ key for b in data)
    try:
        return rezultat.decode("utf-8")
    except UnicodeDecodeError:
        return None

mesaj = "SALUT"
cheie = 42

date_codificate = bytes(ord(c) ^ cheie for c in mesaj)
print(decode_xor(date_codificate, cheie))


def decode_auto(text):
    rezultate = {}

    rezultat_hex = decode_hex(text)
    if rezultat_hex is not None:
        rezultate["Hex"] = rezultat_hex

    rezultat_base64 = decode_base64(text)
    if rezultat_base64 is not None:
        rezultate["Base64"] = rezultat_base64

    rezultat_url = decode_url(text)
    if rezultat_url is not None:
        rezultate["URL"] = rezultat_url

    return rezultate

print(decode_auto("53414c5554"))


def decode_xor_auto(data):
    rezultate = []

    for cheie in range(256):
        rezultat = decode_xor(data, cheie)

        if rezultat is not None and rezultat.isprintable():
            rezultate.append((cheie, rezultat))

    return rezultate


print(decode_xor_auto(date_codificate))

# testare A2
print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))
print(ghici_strat("U2FsdXQ="))

#testare A3
strat, rezultat = desfa("U2FsdXQ=")
print(strat, rezultat)

#testare A4
print(citibil(b"Salut"))
print(citibil(b"\x01\x02"))

val = "NTM1OTU3NTk="
print(decodifica_straturi(val))
print("Rezultat:", decodifica_straturi("NTM1OTU3NTk="))


# A5. Spargerea unui mesaj criptat cu XOR
from pathlib import Path

cale = Path(__file__).resolve().parents[2] / "probe" / "xor.bin"
date = cale.read_bytes()

for k in range(256):
    clar = bytes(b ^ k for b in date)

    if citibil(clar):
        print("Cheie:", k, "| Mesaj:", clar.decode("ascii"))



 # A6. Spargerea unui hash prin dicționar
import hashlib
from pathlib import Path

director = Path(__file__).resolve().parents[2] / "probe"

tinta = (director / "hashuri.txt").read_text().splitlines()[0].strip()

if len(tinta) == 32:
    algoritm = "md5"
elif len(tinta) == 40:
    algoritm = "sha1"
elif len(tinta) == 64:
    algoritm = "sha256"
else:
    algoritm = None

if algoritm is None:
    print("Algoritm de hash necunoscut")
else:
    print("Algoritm:", algoritm)

    for cuv in (director / "wordlist.txt").read_text(
        encoding="latin1"
    ).splitlines():
        hash_cuv = hashlib.new(
            algoritm, cuv.encode("latin1")
        ).hexdigest()

        if hash_cuv == tinta:
            print("Parola găsită:", cuv)
            break
    else:
        print("Parola nu a fost găsită în dicționar")


        # A7. Utilizarea decoderului din terminal
import argparse
import json

def main():
    parser = argparse.ArgumentParser(
        description="Decoder universal pentru șiruri și fișiere"
    )
    parser.add_argument("intrare", help="Șirul de decodat sau calea fișierului")
    parser.add_argument(
        "--fisier",
        action="store_true",
        help="Citește intrarea dintr-un fișier"
    )
    args = parser.parse_args()

    if args.fisier:
        date = Path(args.intrare).read_bytes()
        strat = "fisier"
        rezultat = date.hex()
    else:
        strat, date = desfa(args.intrare)
        rezultat = date.hex()

    fisa = {
        "strat": strat,
        "rezultat": rezultat
    }

    cale_fisa = Path(__file__).with_name("fisa.json")
    cale_fisa.write_text(
        json.dumps(fisa, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    print(json.dumps(fisa, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
    