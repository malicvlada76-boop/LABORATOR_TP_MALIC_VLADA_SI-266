import hashlib
from pathlib import Path

# Folderul în care se vor crea fișierele de laborator
DIRECTOR = Path(__file__).parent

# 1. Mesaj codificat în mai multe straturi
mesaj = "NTM1OTU3NTk="
(DIRECTOR / "mesaj.txt").write_text(mesaj, encoding="utf-8")

# 2. Mesaj criptat cu XOR
mesaj_clar = b"SALUT"
cheie = 42
mesaj_xor = bytes(octet ^ cheie for octet in mesaj_clar)
(DIRECTOR / "xor.bin").write_bytes(mesaj_xor)

# 3. Hash-uri și lista de parole pentru testare
parola = "moldova"
hash_parola = hashlib.md5(parola.encode()).hexdigest()
(DIRECTOR / "hashuri.txt").write_text(
    hash_parola + "\n", encoding="utf-8"
)

cuvinte = ["salut", "parola", "moldova", "student", "python"]
(DIRECTOR / "wordlist.txt").write_text(
    "\n".join(cuvinte) + "\n", encoding="utf-8"
)

print("Fișierele de laborator au fost create în:", DIRECTOR)



# 4. Creăm o fotografie JPEG simplă pentru testare
from PIL import Image
import io
import zipfile

imagine = Image.new("RGB", (100, 100), color="white")
imagine.save(DIRECTOR / "foto.jpg", format="JPEG")

# 5. Creăm un PNG și adăugăm la final o arhivă ZIP
cale_png = DIRECTOR / "ascuns.png"
imagine.save(cale_png, format="PNG")

continut_zip = io.BytesIO()
with zipfile.ZipFile(continut_zip, "w") as arhiva:
    arhiva.writestr(
        "mesaj_secret.txt",
        "Acesta este mesajul ascuns."
    )

with open(cale_png, "ab") as fisier:
    fisier.write(continut_zip.getvalue())

print("Imaginile de test au fost create.")
