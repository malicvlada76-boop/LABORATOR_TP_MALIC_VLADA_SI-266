# EXERCIȚIUL 9
# Elementele de bază ale răspunsului.

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

response = requests.get(BASE_URL, timeout=TIMEOUT)

print(response.status_code) #atribut

print(response.ok)  #atribut

print(response.url) #atribut

print(response.encoding) #atribut



# EXERCIȚIUL 10
# Tratarea erorilor cu o metodă.

response.raise_for_status()

try:
    response = requests.get(
       ECHO_URL + "/status/404",
        timeout=TIMEOUT
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as eroare:
    print("A apărut o eroare:", eroare)



# EXERCIȚIUL 11
# Afișăm toate antetele 

response = requests.get(BASE_URL, timeout=TIMEOUT)

for nume, valoare in response.headers.items():
    print(nume + ": " + valoare)



# EXERCIȚIUL 12
# Metode de dicționar.

print(response.headers.get("Server", "lipsește"))

print(response.headers.get("Content-Type", "lipsește"))

print(response.headers.get("content-type", "lipsește"))

# Observație: numele antetelor HTTP nu țin cont de litere mari sau mici.
# De aceea "Content-Type" și "content-type" returnează aceeași valoare.



# EXERCIȚIUL 13
# Înlănțuirea metodelor de șir.

print(response.text.lower().count("cyber"))

# Putem înlănțui .lower() și .count() deoarece .lower()
# returnează un șir de caractere, iar pe acel șir putem aplica .count().



# EXERCIȚIUL 14
# Găsirea titlului paginii.

html = response.text

start = html.find("<title>") + len("<title>")
end = html.find("</title>")

titlu = html[start:end].strip()

print(titlu)



# EXERCIȚIUL 15
# Numărarea liniilor.

lines = response.text.splitlines()

print("Număr de linii:", len(lines))

cea_mai_lunga = max(lines, key=len)

print("Lungimea celei mai lungi linii:", len(cea_mai_lunga))



# EXERCIȚIUL 16
# Verificăm dacă pagina folosește HTTPS.

if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")



# EXERCIȚIUL 17
# Urmărirea redirecționărilor.

response = requests.get("http://cybercor.org", timeout=TIMEOUT)

for redirection in response.history:
    print(redirection.status_code, redirection.url)

print("URL final:", response.url)    



# EXERCIȚIUL 18
# HEAD versus GET.

raspuns_head = requests.head(BASE_URL, timeout=TIMEOUT)

raspuns_get = requests.get(BASE_URL, timeout=TIMEOUT)

print("HEAD:", len(raspuns_head.content))
print("GET:", len(raspuns_get.content))

# Cererea HEAD primește doar informații despre resursă și nu primește corpul paginii.
# Cererea GET primește și corpul paginii, de aceea conținutul este mult mai mare.



# EXERCIȚIUL 19
# Cookie-uri.

if response.cookies:
    for cookie in response.cookies:
        print("Nume:", cookie.name)
        print("Secure:", cookie.secure)
else:
    print("Niciun cookie setat.")


# EXERCIȚIUL 20
# Sesiuni.

session = requests.Session()

session.headers.update({
    "User-Agent": "WebLab-Vlada"
})

response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)

print(response.text)

# response.text este un atribut, de aceea nu are paranteze.
# response.json() este o metodă, de aceea are paranteze.
# Ambele ne oferă corpul răspunsului, dar în forme diferite.