import requests
import time

TIMEOUT = 10

# Antetul folosit la cererile HTTP.
DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Malic-Vlada"
}


# Exercițiul 44. Funcție pentru efectuarea unei cereri HTTP.
def fetch(url, timeout=TIMEOUT):
    """Trimite o cerere GET și returnează răspunsul."""
    response = requests.get(
        url,
        timeout=timeout,
        headers=DEFAULT_HEADERS
    )
    return response


# Exercițiul 44. Funcție care returnează codul de stare.
def get_status(url):
    """Returnează codul de stare HTTP."""
    response = fetch(url)
    return response.status_code


# Exercițiul 44. Funcție care extrage titlul paginii.
def get_title(html):
    """Returnează titlul paginii din codul HTML."""
    start = html.find("<title>")
    end = html.find("</title>")

    if start == -1 or end == -1:
        return "Titlu negăsit"

    start += len("<title>")
    return html[start:end].strip()


# Exercițiul 44. Verifică antetele de securitate.
def security_headers(url):
    """Verifică prezența unor antete de securitate."""
    response = fetch(url)
    headers = response.headers

    required_headers = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy"
    ]

    results = {}

    for name in required_headers:
        results[name] = name in headers

    return results


# Exercițiul 46. Autotestul rulează doar dacă fișierul
# webtools.py este executat direct.
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))


# Exercițiul 49. Verificăm mai multe căi ale site-ului.
def check_paths(base, paths):
    """Returnează codul de stare pentru fiecare cale."""
    results = {}

    for path in paths:
        response = fetch(base.rstrip("/") + path)
        results[path] = response.status_code
        time.sleep(1)

    return results

# Exercițiul 50. Construim un raport despre site.
def site_report(url):
    """Colectează informații despre site și returnează un dicționar."""
    import json
    import socket
    import ssl
    from datetime import datetime
    from urllib.parse import urlparse

    response = fetch(url)
    html = response.text
    parsed_url = urlparse(response.url)
    hostname = parsed_url.hostname

    # Verificăm antetele de securitate.
    headers = security_headers(response.url)
    score = sum(headers.values())

    # Determinăm adresa IP a site-ului.
    try:
        ip_address = socket.gethostbyname(hostname)
    except (socket.gaierror, TypeError):
        ip_address = "Indisponibil"

    # Verificăm câte zile mai este valabil certificatul TLS.
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                cert = secure_sock.getpeercert()

        expiry = datetime.strptime(
            cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
        )
        days_left = (expiry - datetime.utcnow()).days
    except (OSError, ValueError, KeyError, ssl.SSLError):
        days_left = None

    # Numărăm linkurile interne și externe.
    from html.parser import HTMLParser

    class LinkParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = []

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                href = dict(attrs).get("href")
                if href:
                    self.links.append(href)

    parser = LinkParser()
    parser.feed(html)

    internal_links = 0
    external_links = 0

    for link in parser.links:
        if link.startswith("/") or hostname in link:
            internal_links += 1
        elif link.startswith(("http://", "https://")):
            external_links += 1

    # Citim robots.txt.
    robots = fetch(parsed_url.scheme + "://" + hostname + "/robots.txt").text
    blocked_paths = []

    for line in robots.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            if path:
                blocked_paths.append(path)

    report = {
        "status_code": response.status_code,
        "final_url": response.url,
        "title": get_title(html),
        "ip_address": ip_address,
        "redirect_chain": [item.url for item in response.history],
        "security_headers_score": f"{score}/{len(headers)}",
        "tls_days_left": days_left,
        "internal_links": internal_links,
        "external_links": external_links,
        "robots_disallowed_paths": blocked_paths
    }

    return report

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
