# -*- coding: utf-8 -*-
"""Laboratorul 7 - enumerare spre root. Generat din programul
de laborator, cu codul scris de student."""
import argparse, io, json, os

GTFO = {'perl', 'python3', 'nmap', 'find', 'cp', 'vim', 'awk', 'less', 'vim.basic', 'bash'}

#  PARTEA A - aduna si grupeaza
# ---------------------------------------------------------------------------

def citeste_linii(cale):
    """Sarcina 1. Citeste un fisier si intoarce LISTA randurilor folositoare.

    Fiecare rand se curata de spatiile de la capete. Se arunca randurile
    goale si cele care incep cu diez, fiindca sunt comentarii.

    citeste_linii("start/suid.txt")  ->  lista cu 14 randuri
    """
   # Cream lista in care vom pastra randurile folositoare.
    linii = []

    # Deschidem fisierul pentru citire.
    with open(cale, "r", encoding="utf-8") as fisier:

        # Parcurgem fiecare rand din fisier.
        for rand in fisier:

            # Eliminam spatiile si caracterul de rand nou de la capete.
            rand = rand.strip()
             # Pastram doar randurile care nu sunt goale sau comentarii.
            if rand != "" and not rand.startswith("#"):
                linii.append(rand)

    # Returnam lista dupa citirea tuturor randurilor.
    return linii


def nume(cale):
    """Sarcina 2. Intoarce numele fisierului dintr-o cale.

    Numele decide daca binarul e periculos, nu toata calea.

    nume("/usr/bin/find")  ->  "find"
    """
    # Despartim la ultimul slash si returnam ultima bucata.
    return cale.rsplit("/", 1)[-1]


def suid_constatari(cale):
    """Sarcina 3. Din fisierul SUID face o LISTA DE DICTIONARE.

    Fiecare cale UNICA, in ordine sortata, devine o fisa cu trei campuri:
        {"cale": ..., "nume": ..., "risc": "mare" sau "normal"}
    Riscul e "mare" daca numele se afla in multimea GTFO, altfel "normal".

    Atentie: in captura o cale apare de doua ori. Fisa ei apare o data.
    """
  # Citim randurile folositoare cu functia de la sarcina 1.
    randuri = citeste_linii(cale)

    # Eliminam dublurile si sortam caile.
    cai_sortate = sorted(set(randuri))

    # Pregatim lista in care vom adauga dictionarele.
    constatari = []

    for cale_fisier in cai_sortate:
        # Extragem numele folosind functia de la sarcina 2.
        nume_fisier = nume(cale_fisier)
        # Stabilim riscul dupa regula ceruta in laborator.
        if nume_fisier in GTFO:
            risc = "mare"
        else:
            risc = "normal"

        # Construim dictionarul pentru fisierul curent.
        constatare = {
            "cale": cale_fisier,
            "nume": nume_fisier,
            "risc": risc
        }

        # Adaugam dictionarul in lista.
        constatari.append(constatare)
    return constatari



def sudo_constatari(cale):
    """Sarcina 4. Din fisierul sudo face o lista de dictionare.

    Un rand are forma  utilizator : drept
    Il despachetezi intr-un tuplu de doua valori, taind la PRIMUL separator:
        user, drept = rand.split(" : ", 1)

    Fiecare rand devine:
        {"user": ..., "drept": ..., "risc": "mare" sau "normal"}
    Riscul e "mare" daca in drept apare NOPASSWD, fiindca atunci comanda
    se ruleaza fara sa se ceara parola.
    """
   # Citim randurile din fisier.
    randuri = citeste_linii(cale)

    # Cream o lista goala pentru rezultate.
    constatari = []

    for rand in randuri:
        # Separam utilizatorul de dreptul sau.
        user, drept = rand.split(" : ", 1)

        # Stabilim riscul.
        if "NOPASSWD" in drept:
            risc = "mare"
        else:
            risc = "normal"

        # Cream un dictionar pentru randul curent.
        constatare = {
            "user": user,
            "drept": drept,
            "risc": risc
        }

        # Adaugam dictionarul in lista.
        constatari.append(constatare)

    return constatari


def cron_constatari(cale):
    """Sarcina 5. Din crontab face o lista de dictionare.

    Un rand de crontab are cinci campuri de timp, apoi utilizatorul si
    comanda. Desparti randul in campuri cu split(), iar:
        campul 5 (al saselea) este utilizatorul
        tot ce urmeaza, lipit la loc cu spatii, este comanda

    Fiecare rand devine:  {"user": ..., "comanda": ...}
    """
   # Citim randurile folositoare.
    randuri = citeste_linii(cale)

    # Pregatim lista rezultatelor.
    constatari = []

    for rand in randuri:
        # Despartim randul la spatii si taburi.
        campuri = rand.split()

        # Al saselea element este utilizatorul.
        user = campuri[5]

        # Lipim toate elementele ramase pentru a reface comanda.
        comanda = " ".join(campuri[6:])

        # Construim dictionarul.
        constatare = {
            "user": user,
            "comanda": comanda
        }

        # Adaugam dictionarul in lista.
        constatari.append(constatare)

    return constatari


def enumereaza(dosar):
    """Sarcina 6. Aduna toate constatarile intr-un singur DICTIONAR.

    Primeste calea folderului cu capturi si intoarce un dictionar cu o
    cheie pe categorie, iar valoarea este lista de constatari:

        {"suid": [...], "sudo": [...], "cron": [...]}

    Pentru a lipi calea unui fisier de folder, foloseste os.path.join.
    """
   # Construim caile catre cele trei fisiere.
    cale_suid = os.path.join(dosar, "suid.txt")
    cale_sudo = os.path.join(dosar, "sudo.txt")
    cale_cron = os.path.join(dosar, "crontab.txt")

    # Prelucram fisierele cu functiile deja scrise.
    suid = suid_constatari(cale_suid)
    sudo = sudo_constatari(cale_sudo)
    cron = cron_constatari(cale_cron)

    # Adunam rezultatele intr-un singur dictionar.
    raport = {
        "suid": suid,
        "sudo": sudo,
        "cron": cron
    }

    return raport


def utilizatori_implicati(raport):
    """Sarcina 7. Intoarce MULTIMEA utilizatorilor care apar in raport.

    Sunt utilizatorii din constatarile sudo REUNITI cu cei din cron.
    Reuniunea a doua multimi se face cu operatorul  |  si arunca dublurile.

    Primeste dictionarul intors de enumereaza.
    """
    # Extragem utilizatorii din sudo si cron.
    sudo_useri = {c["user"] for c in raport["sudo"]}
    cron_useri = {c["user"] for c in raport["cron"]}

    # Reunim cele doua multimi.
    utilizatori = sudo_useri | cron_useri

    return utilizatori


# ---------------------------------------------------------------------------
#  PARTEA B - ce e nou fata de un sistem curat
# ---------------------------------------------------------------------------

def cai(fisier):
    """Sarcina 8. Intoarce MULTIMEA cailor dintr-un fisier.

    Foloseste citeste_linii, pe care ai scris-o deja la sarcina 1.
    O multime arunca singura dublurile, de aceea aici iese 13, nu 14.
    """
    # Citim randurile folositoare din fisier.
    randuri = citeste_linii(fisier)

    # Transformam lista in multime pentru a elimina dublurile.
    multime_cai = set(randuri)

    return multime_cai


def suid_noi(acum, baza):
    """Sarcina 9. Ce e in acum, dar nu si in baza.

    Amandoua sunt multimi de cai. Rezultatul este tot o multime: fisierele
    SUID aparute fata de sistemul curat.

    Se face cu UN SINGUR operator, nu cu doua bucle una in alta.
    """
    # Folosim operatorul de diferenta pentru a obtine fisierele noi.
    noi = acum - baza

    return noi


def risc_pe_nume(multime_cai):
    """Sarcina 10. Fisa nume -> risc, ca DICTIONAR.

    Pentru fiecare cale din multimea primita, cheia este numele fisierului,
    iar valoarea este "mare" daca numele se afla in GTFO, altfel "normal".

    Se scrie pe un singur rand, cu dict comprehension.
    """
    # Construim dictionarul folosind dict comprehension.
    return {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in multime_cai}


def periculoase_noi(noi):
    """Sarcina 11. Lista cailor noi care sunt periculoase, sortata.

    Din multimea primita pastrezi doar caile al caror nume e in GTFO si le
    intorci ca lista, in ordine sortata.
    """
    # Filtram caile periculoase si le sortam.
    periculoase = sorted([c for c in noi if nume(c) in GTFO])

    return periculoase


# ===========================================================================
#
#   Sub randul urmator incepe programul care te verifica.
#   Nu e nevoie sa intelegi codul de mai jos si nu il modifica.
#
# ===========================================================================
#  


def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print("%s: %d gasite, %d cu risc mare" % (categorie, len(lista), len(mari)))
    useri = utilizatori_implicati(raport)
    print("utilizatori implicati:", ", ".join(sorted(useri)))
    with io.open("enum.json", "w", encoding="utf-8") as fis:
        json.dump(raport, fis, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
