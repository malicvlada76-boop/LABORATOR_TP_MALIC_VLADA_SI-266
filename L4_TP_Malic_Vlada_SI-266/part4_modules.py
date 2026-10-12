import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


# Exercițiul 35
# Folosiți urllib.parse.urlparse() pe URL-ul
# https://cybercor.org/path?x=1#top.
# Afișați scheme, netloc, path, query și fragment.

from urllib.parse import urlparse

from part1_imports import BASE_URL

def descompune_url(url):
  
    rezultat = urlparse(url)

    print("scheme:", rezultat.scheme)
    print("netloc:", rezultat.netloc)
    print("path:", rezultat.path)
    print("query:", rezultat.query)
    print("fragment:", rezultat.fragment)

descompune_url("https://cybercor.org/path?x=1#top")




# Exercițiul 36
# Folosiți urllib.parse.urljoin() pentru a transforma
# legăturile relative /about, contact.html și ../index.html
# în URL-uri complete, pornind de la BASE_URL.

from urllib.parse import urljoin

def compune_urluri(base_url):

    legaturi = ["/about", "contact.html", "../index.html"]

    for legatura in legaturi:
        url_complet = urljoin(base_url, legatura)
        print(url_complet)


compune_urluri(BASE_URL)





# Exercițiul 37
# Folosiți re.findall(r'href="([^"]+)"', html)
# pentru a obține toate legăturile de pe pagina principală.
# Funcția extract_links(html) trebuie să returneze legăturile
# fără duplicate.

import re
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

def extract_links(html):

    legaturi = re.findall(r'href="([^"]+)"', html)

    legaturi_unice = list(dict.fromkeys(legaturi))

    return legaturi_unice

raspuns = requests.get(BASE_URL, timeout=TIMEOUT)

html = raspuns.text

print(extract_links(html))





# Exercițiul 38
# Scrieți funcția split_links(links, domain),
# care returnează două liste: legăturile de pe același domeniu
# și legăturile către alte site-uri.
# Folosiți mai întâi urljoin(), apoi urlparse().netloc.

from urllib.parse import urljoin, urlparse

def split_links(links, domain):
    interne = []
    externe = []

    for link in links:

        url_complet = urljoin(domain, link)

        domeniu_link = urlparse(url_complet).netloc

        if domeniu_link == urlparse(domain).netloc:

            interne.append(url_complet)
        else:
            externe.append(url_complet)

    return interne, externe


legaturi = [
    "/about",
    "https://example.com/page",
    "/contact",
    "https://www.wikipedia.org"
]

interne, externe = split_links(legaturi, BASE_URL)

print("Legături interne:", interne)
print("Legături externe:", externe)





# Exercițiul 39
# Creați o clasă care moștenește HTMLParser
# și suprascrie metoda handle_starttag() pentru a colecta
# atributul src al fiecărui tag <img>.
# Testăm mai întâi pe un fragment HTML cunoscut,
# apoi folosim parserul pe pagina principală.

from html.parser import HTMLParser

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
         atribute= dict(attrs)
         src = atribute.get("src")
         if src is not None:
               self.images.append(src)


# Etapa 1. Testăm parserul pe un HTML cunoscut.
test_html = """
<html><body>
    <img src="/logo.png" alt="Logo">
    <IMG SRC="poza.jpg">
    <img alt="imagine fără src">
    <img src="https://cdn.example.com/banner.webp" />
    <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)

print("Imagini din test:", finder.images)

# Verificăm dacă au fost găsite exact imaginile așteptate.
assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp"
], "Parserul nu a găsit exact imaginile așteptate"

print("Testul a trecut!")


# Etapa 2. Folosim parserul pe pagina principală.
# Așteptăm o secundă înaintea unei noi cereri HTTP.
time.sleep(1)


response = requests.get(BASE_URL, timeout=TIMEOUT)
response.raise_for_status()

finder = ImageFinder()
finder.feed(response.text)

print(len(finder.images), "imagini găsite")

for src in finder.images:
    print(src)

# Comparăm rezultatul cu numărul de taguri <img> din HTML.
numar_taguri = response.text.lower().count("<img")
print("Număr de taguri <img> în HTML:", numar_taguri)





# Exercițiul 40
# Scrieți funcția page_fingerprint(url), care returnează
# hashlib.sha256(response.content).hexdigest().
# Rulați funcția de două ori și comparați rezultatele.
# Explicați când ar putea fi diferite.

import hashlib
import time

def page_fingerprint(url):

    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    amprenta = hashlib.sha256(response.content).hexdigest()
    return amprenta


amprenta1 = page_fingerprint(BASE_URL)
print("Prima amprentă:", amprenta1)

time.sleep(1)

amprenta2 = page_fingerprint(BASE_URL)
print("A doua amprentă:", amprenta2)

if amprenta1 == amprenta2:
    print("Amprentele sunt identice.")
else:
    print("Amprentele sunt diferite.")





# Exercițiul 41
# Salvați antetele paginii principale în headers.json
# folosind json.dump(dict(response.headers), file, indent=2).
# Apoi încărcați fișierul cu json.load() și afișați un antet.

import json
import time

response = requests.get(BASE_URL, timeout=TIMEOUT)
response.raise_for_status()

with open("headers.json", "w", encoding="utf-8") as file:
    json.dump(dict(response.headers), file, indent=2)

print("Antetele au fost salvate în headers.json.")


with open("headers.json", "r", encoding="utf-8") as file:
    antete = json.load(file)

print("Server:", antete.get("Server", "Antetul nu există"))




# Exercițiul 42
# Scrieți funcția resolve(hostname), care returnează
# socket.gethostbyname(hostname).
# Afișați adresa IP a domeniului cybercor.org.

import socket

def resolve(hostname):
    return socket.gethostbyname(hostname)

ip = resolve("cybercor.org")
print("Adresa IP a domeniului cybercor.org:", ip)




# Exercițiul 43
# Scrieți funcția cert_days_left(hostname), care se conectează
# la portul 443, citește certificatul și returnează numărul de zile
# rămase până la expirarea acestuia.

import ssl
import socket

def cert_days_left(hostname):
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as conexiune:
            certificat = conexiune.getpeercert()

    data_expirarii = ssl.cert_time_to_seconds(certificat["notAfter"])
    zile_ramase = int((data_expirarii - time.time()) / 86400)

    return zile_ramase


zile = cert_days_left("cybercor.org")
print("Zile rămase până la expirarea certificatului:", zile)

#Verificati-va:
#nu apelăm direct handle_starttag(),deoarece HTMLParser o apelează automat
#în timpul analizării codului HTML.