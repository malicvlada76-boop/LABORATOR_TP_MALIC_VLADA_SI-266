# Laborator: funcții, metode și importuri pe web
# Student: < Malic Vlada >

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10   #secunde

# EXERCIȚIUL 1
# Primul import.
# Importăm requests și afișăm versiunea sa.
# Apoi importăm urllib.request.
# Explicăm de ce requests trebuie instalat cu pip,
# iar urllib nu trebuie instalat separat.

import requests

print(requests.__version__)

import urllib.request

# requests este o bibliotecă externă și trebuie instalată cu pip.
# urllib face parte deja din Python, de aceea nu trebuie instalată separat.




# EXERCIȚIUL 2
# Descărcăm pagina BASE_URL cu requests.get()
# Afișăm codul de stare.
# Varianta 1 -requests.get()
import requests

raspuns = requests.get(BASE_URL, timeout=TIMEOUT)

print(raspuns.status_code)

# Avantaj: requests.get() este clar și ușor de înțeles
# atunci când folosim mai multe funcții din biblioteca requests.

# Varianta 2 - from requests import get

from requests import get

raspuns = get(BASE_URL, timeout=TIMEOUT)

print(raspuns.status_code)

# Avantaj: putem scrie direct get(), fără requests.get().




# EXERCIȚIUL 3
# Importăm requests cu aliasul rq
# Descărcăm pagina principală cu rq.get()

import requests as rq

raspuns = rq.get(BASE_URL, timeout=TIMEOUT)

print(raspuns.status_code)

# Un alias face codul mai ușor de citit atunci când numele bibliotecii
# este lung sau este folosit de multe ori.
# Un alias poate face codul mai greu de citit dacă nu este clar
# ce bibliotecă reprezintă aliasul.




# EXERCIȚIUL 4
# Descărcăm pagina principală folosind urllib.request.urlopen().
# Afișăm codul de stare și primele 200 de caractere din corp.

import urllib.request

cerere = urllib.request.Request(
    BASE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)
# Am folosit User-Agent deoarece cererea simplă cu urllib.request.urlopen()
# era respinsă de server cu eroarea 403 Forbidden.
# Cu ajutorul AI am identificat problema și am ajustat cererea.

raspuns = urllib.request.urlopen(cerere, timeout=TIMEOUT)

print(raspuns.status)

continut = raspuns.read().decode("utf-8")

print(continut[:200])




# EXERCIȚIUL 5
# Privim numele disponibile în modulul requests.

print(dir(requests))

# get - funcție, folosită pentru a face cereri HTTP de tip GET.
# Response - clasă, reprezintă răspunsul primit de la server.
# sessions - modul, care conține funcționalități pentru gestionarea sesiunilor.



# EXERCIȚIUL 6
# Afișăm documentația funcției requests.get.

help(requests.get)

raspuns = requests.get(BASE_URL, timeout=TIMEOUT)

print(raspuns.status_code)

# Parametrul timeout stabilește timpul maxim de așteptare pentru răspuns.



# EXERCIȚIUL 7
# Măsurăm cât durează o cerere către pagina principală.
# Compararea rezultatului cu response.elapsed

import time

start = time.perf_counter()

response = requests.get(BASE_URL, timeout=TIMEOUT)

end = time.perf_counter()

print("Timpul cererii:", end - start, "secunde")

print("Timpul serverului:", response.elapsed.total_seconds(), "secunde")

# end - start măsoară timpul total al cererii.
# response.elapsed arată timpul măsurat de requests pentru răspunsul serverului.
# Timpul cererii: aproximativ 0.1054 secunde
# Timpul serverului: aproximativ 0.1046 secunde,valori foarte apropiate



# EXERCIȚIUL 8
# Verificăm cand un import esueaza.

try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4.")

# Modul - un fișier Python cu cod reutilizabil.
# Pachet - un grup de module organizate împreună.
# Bibliotecă - o colecție de coduri reutilizabile.