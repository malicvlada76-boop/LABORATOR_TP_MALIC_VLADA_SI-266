import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10 # secunde

# Exercițiul 21
# Scrieți fetch(url), care returnează obiectul răspuns.
# Apelați funcția pentru BASE_URL și afișați codul de stare.

def fetch(url):
    response = requests.get(url, timeout=TIMEOUT)
    return response

response = fetch(BASE_URL)
print(response.status_code)

# Funcția fetch primește un URL și face o cerere GET.
# return response întoarce răspunsul.



# Exercițiul 22
# Scrieți get_status(url), care returnează doar codul de stare.
# Apelați-o pentru /, /robots.txt și /sitemap.xml, cu time.sleep(1) între apeluri.

def get_status(url):
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

print(get_status(BASE_URL + "/"))
time.sleep(1)

print(get_status(BASE_URL + "/robots.txt"))
time.sleep(1)

print(get_status(BASE_URL + "/sitemap.xml"))

# Funcția primește un URL și returnează doar codul de stare.



# Exercițiul 23
# Modificați funcția în fetch(url, timeout=10).
# Apelați-o o dată cu valoarea implicită și o dată cu timeout=3.

def fetch(url, timeout=10):
    response = requests.get(url, timeout=timeout)
    return response

print(fetch(BASE_URL).status_code)
print(fetch(BASE_URL, timeout=3).status_code)

# Dacă nu specificăm timeout, se folosește valoarea 10.
# Putem însă să transmitem o altă valoare, de exemplu 3.



# Exercițiul 24
# Scrieți get_title(html), care primește un șir HTML
# și returnează titlul paginii.

def get_title(html):
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    titlu = html[start:end].strip()
    return titlu

html = fetch(BASE_URL).text
print(get_title(html))

# Folosim aceeași logică din Exercițiul 14,
# dar o punem într-o funcție.



# Exercițiul 25
#  Adăugați un docstring funcției get_title
# și afișați-l cu help(get_title).

def get_title(html):
    """Returnează titlul paginii din codul HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    titlu = html[start:end].strip()
    return titlu

html = fetch(BASE_URL).text
print(get_title(html))
help(get_title)

# Docstring-ul descrie ce face funcția.
# help(get_title) afișează această descriere.





# Exercițiul 26
#Să se adauge adnotări de tip (type hints) funcțiilor.
# Să se definească funcția get_status(url: str) -> int.
# Să se apeleze funcția cu argumentul get_status(123) și să se observe
# dacă adnotările de tip opresc executarea programului.

def get_status(url: str) -> int:
    return 200

print(get_status("https://example.com"))

print(get_status(123))

help(get_status)
# url: str indică faptul că parametrul este așteptat să fie text.



# Exercițiul 27
#Să se scrie funcția page_exists(url), care verifică dacă o pagină web
# poate fi accesată și returnează True sau False.
# Se va utiliza try/except requests.RequestException pentru a gestiona
# erorile și a evita oprirea programului, inclusiv în cazul unui URL inexistent.

def page_exists(url):
    try:
        raspuns = requests.get(url, timeout=TIMEOUT)
        return raspuns.status_code < 400

    except requests.RequestException:
        return False


print(page_exists("https://httpbin.org/get"))

print(page_exists("https://this-domain-does-not-exist.invalid"))




# Exercițiul 28
#  Scrieți funcția check_paths(base, paths), care primește
# o adresă de bază și o listă de căi, de exemplu ["/", "/robots.txt",
# "/sitemap.xml"], și returnează un dicționar de forma
# {path: status_code}, în care fiecare cale este asociată cu codul
# de stare HTTP primit.

def check_paths(base, paths):
    rezultate = {}

    for path in paths:
        try:
            url = base.rstrip("/") + "/" + path.lstrip("/")

            raspuns = requests.get(url, timeout=TIMEOUT)

            rezultate[path] = raspuns.status_code

        except requests.RequestException:

            rezultate[path] = None

    
            time.sleep(1)


    return rezultate


base = "https://httpbin.org"
paths = ["/", "/robots.txt", "/sitemap.xml"]

print(check_paths(base, paths))




# Exercițiul 29
# Să se scrie funcția get_header(url, name, default="lipsește"),
# care returnează valoarea unui singur antet HTTP.
# Funcția va fi apelată cu argumente cu nume, folosind:
# get_header(BASE_URL, name="Server").

def get_header(url, name, default="lipsește"):
    try:
        raspuns = requests.get(url, timeout=TIMEOUT)

        valoare = raspuns.headers.get(name)

        if valoare is not None:
            return valoare

        return default

    except requests.RequestException:

        return default

print(get_header(BASE_URL, name="Server"))



# Exercițiul 30
# Să se scrie funcția security_headers(url), care verifică
# prezența a cinci antete de securitate HTTP și returnează un dicționar
# de forma {antet: True/False}, unde True indică prezența antetului,
# iar False indică absența acestuia.

def security_headers(url):
    antete = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    try:
        raspuns = requests.get(url, timeout=TIMEOUT)

        rezultate = {}
        for antet in antete:
            rezultate[antet] = antet in raspuns.headers

        return rezultate

    except requests.RequestException:
        return {antet: False for antet in antete}

print(security_headers(BASE_URL))




# Exercițiul 31
# Să se scrie funcția score_headers(results), care primește
# dicționarul returnat de funcția security_headers() din exercițiul 30
# și returnează un șir de caractere de forma "3/5", care indică
# numărul antetelor de securitate prezente din totalul de cinci.
# Apelați funcțiile împreună folosind:
# score_headers(security_headers(BASE_URL)).

def score_headers(results):

    prezente = sum(results.values())

    return f"{prezente}/5"

print(score_headers(security_headers(BASE_URL)))




# Exercițiul 32
# Să se scrie funcția fetch_robots(base), care returnează
# textul fișierului /robots.txt sau None dacă fișierul lipsește.
# Apoi, să se scrie funcția disallowed_paths(robots_text), care
# returnează o listă cu toate valorile indicate prin Disallow:.
# Funcția disallowed_paths() trebuie să funcționeze și când primește None.

def fetch_robots(base):
    try:
        url = base.rstrip("/") + "/robots.txt"

        raspuns = requests.get(url, timeout=TIMEOUT)

        if raspuns.status_code == 200:
            return raspuns.text

        return None

    except requests.RequestException:
        return None


# Definim funcția care extrage căile Disallow.
def disallowed_paths(robots_text):
    if robots_text is None:
        return []

    cai = []

    for linie in robots_text.splitlines():

        linie = linie.strip()

        if linie.lower().startswith("disallow:"):

            cale = linie.split(":", 1)[1].strip()

            cai.append(cale)

    return cai

robots_text = fetch_robots(BASE_URL)

print(disallowed_paths(robots_text))

print(disallowed_paths(None))




# Exercițiul 33
# Să se scrie funcția response_times(*urls), care primește
# un număr variabil de URL-uri și returnează un dicționar de forma
# {url: secunde}, în care fiecare adresă este asociată cu timpul
# necesar pentru efectuarea cererii HTTP.
# Apelați funcția cu două URL-uri.

def response_times(*urls):
    rezultate = {}

    for url in urls:
        try:
            inceput = time.perf_counter()

            requests.get(url, timeout=TIMEOUT)

            durata = time.perf_counter() - inceput

            rezultate[url] = round(durata, 3)

        except requests.RequestException:
            rezultate[url] = None

        time.sleep(1)

    return rezultate

print(response_times(BASE_URL, ECHO_URL))


# Rezultatul afișează timpul necesar pentru obținerea unui răspuns
# de la fiecare server. Timpii sunt măsurați în secunde și pot
# varia în funcție de conexiunea la internet și de răspunsul serverului.




# Exercițiul 34
# Să se scrie funcția log(message, **details), care afișează
# mesajul urmat de fiecare detaliu primit ca argument cu nume.
# Exemplu: log("verificat", url=BASE_URL, status=200) trebuie să afișeze:
# verificat | url=https://cybercor.org | status=200

def log(message, **details):

    parti = [message]

    for cheie, valoare in details.items():

        parti.append(f"{cheie}={valoare}")

    print(" | ".join(parti))

log("verificat", url=BASE_URL, status=200)


# Verificați diferența dintre afișarea unei valori cu print()
# în interiorul unei funcții și returnarea acesteia cu return.


#Diferența dintre print() și return:
#print() afișează o valoare pe ecran, dar nu o oferă ca rezultat al funcției
#return transmite valoarea înapoi către locul de unde a fost apelată funcția,