
from pathlib import Path
import subprocess
import zipfile

from PIL import Image
from PIL.ExifTags import TAGS


# B1. Identificăm tipul fișierelor din folderul probe.
def identifica_fisiere(folder="probe"):
    print("\n=== B1: IDENTIFICAREA FIȘIERELOR ===")

    for cale in sorted(Path(folder).iterdir()):
        if cale.is_file():
            rezultat = subprocess.run(
                ["file", str(cale)],
                capture_output=True,
                text=True
            )
            print(rezultat.stdout.strip())


# B2. Citim metadatele EXIF și verificăm existența GPS.
def citeste_exif(cale):
    print("\n=== B2: METADATE EXIF ȘI GPS ===")

    imagine = Image.open(cale)
    exif = imagine.getexif()

    print("Imagine:", cale)
    print("Format:", imagine.format)
    print("Dimensiuni:", imagine.size)

    if not exif:
        print("Imaginea nu conține metadate EXIF.")
        print("Nu sunt disponibile coordonate GPS.")
        return

    gps_gasit = False

    for id_tag, valoare in exif.items():
        nume_tag = TAGS.get(id_tag, id_tag)
        print(f"{nume_tag}: {valoare}")

        if nume_tag == "GPSInfo":
            gps_gasit = True

    if gps_gasit:
        print("Imaginea conține informații GPS.")
    else:
        print("Nu au fost găsite informații GPS.")


# B3. Căutăm arhiva ZIP ascunsă în fișierul PNG.
def cauta_zip(cale):
    print("\n=== B3: DETECTAREA ARHIVEI ZIP ===")

    try:
        with zipfile.ZipFile(cale, "r") as arhiva:
            print("Am găsit o arhivă ZIP!")

            for nume in arhiva.namelist():
                print("-", nume)

            return True

    except zipfile.BadZipFile:
        print("Nu a fost găsită o arhivă ZIP validă.")
        return False


# B4. Extragem fișierele din arhiva ZIP.
def extrage_zip(cale, destinatie="probe/extras"):
    print("\n=== B4: EXTRAGEREA ARHIVEI ===")

    try:
        with zipfile.ZipFile(cale, "r") as arhiva:
            arhiva.extractall(destinatie)
            print("Fișiere extrase în:", destinatie)

            for nume in arhiva.namelist():
                print("-", nume)

    except zipfile.BadZipFile:
        print("Extragerea nu a reușit: arhiva ZIP nu este validă.")


# Executăm toate operațiile.
if __name__ == "__main__":
    identifica_fisiere()
    citeste_exif("probe/foto.jpg")

    if cauta_zip("probe/ascuns.png"):
        extrage_zip("probe/ascuns.png")
