# Partea 1:Functii
import requests 
import time

#1
def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    return f"{host.rstrip('/')}/{path.lstrip('/')}"
print(build_url("https://example.com", "/login"))  # https://example.com/login
#2
def is_https(url):
    if url.startswith("https://"):
        return True
    else:
        return False

print(is_https("https://example.com"))  # True
print(is_https("http://example.com"))   # False

#Partea 2:Trimiterea unei cereri

def show_response(url):

    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

print(show_response("https://httpbin.org/html"))  # Status: 200, Content-Type: text/html; charset=utf-8

#Partea 3: Un verificator reutilizabil
timeout = 5  # Timeout de 5 secunde pentru cereri
def check_site(url):
    try:
        response = requests.get(url, timeout=timeout)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type"),
            "length": len(response.content),
            "server": response.headers.get("Server"),
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": None,
            "content_type": None,
            "length": None,
            "server": None,
            "error": str(e),
        }

    
#Partea 4: Verificarea mai multor site-uri
def scan_sites():
    results = []
    for url in sites:
        result = check_site(url)
        results.append((url, result))
        if result.status_code == 200:
            print(f"{url} is up. Status: {result.status_code}")
    return results
 