import argparse
import time
import webtools

from webtools import get_title, security_headers, DEFAULT_HEADERS

# Exercițiul 48. Primim adresa site-ului din linia de comandă.
parser = argparse.ArgumentParser(description="Verificarea unui site web")
parser.add_argument("url", help="Adresa site-ului care va fi verificat")
args = parser.parse_args()

url = args.url

# Exercițiul 44. Folosim funcțiile din modulul webtools.
response = webtools.fetch(url)
print("Cod de stare:", response.status_code)
print("URL final:", response.url)
print("Titlul paginii:", webtools.get_title(response.text))

# Exercițiul 45. Importăm și folosim funcțiile direct.
print("Titlul paginii:", get_title(response.text))
print("Antete de securitate:", security_headers(url))

# Exercițiul 45. Dacă definim aici o funcție proprie numită get_title,
# aceasta poate ascunde numele importat și poate crea confuzie.

# Exercițiul 47. Afișăm antetele implicite.
print("Antete implicite:", DEFAULT_HEADERS)

# Exercițiul 49. Salvăm rezultatele verificării în report.csv.
import csv
from datetime import datetime

paths = webtools.check_paths(url, ["/", "/robots.txt", "/sitemap.xml"])

with open("report.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["path", "status", "checked_at"]
    )
    writer.writeheader()

    for path, status in paths.items():
        writer.writerow({
            "path": path,
            "status": status,
            "checked_at": datetime.now().isoformat()
        })

        time.sleep(1)

print("Raportul CSV a fost salvat în report.csv")


# Exercițiul 50. Generăm și salvăm raportul JSON.
import json

report = webtools.site_report(url)

print(json.dumps(report, indent=4, ensure_ascii=False))

with open("report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4, ensure_ascii=False)

print("Raportul JSON a fost salvat în report.json")
