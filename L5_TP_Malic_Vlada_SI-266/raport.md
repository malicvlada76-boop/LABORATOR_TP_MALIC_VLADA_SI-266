# Laboratorul 5 — Informații invizibile: forensics și steganografie

## 1. Scopul lucrării

Scopul lucrării este studierea metodelor de identificare, decodificare și analiză a fișierelor, precum și înțelegerea modului în care informațiile pot fi ascunse în imagini.

## 2. Partea A — Decodificare

Au fost implementate funcții pentru transformarea textului în bytes și hex, identificarea codificărilor URL, hex și Base64 și decodificarea mai multor straturi.

De asemenea, au fost realizate funcții pentru identificarea cheilor XOR prin încercarea tuturor valorilor posibile și pentru verificarea hashurilor cu ajutorul unui dicționar.

Rezultate obținute:
- Mesajul Base64 `U2FsdXQ=` a fost decodificat în `Salut`.
- Mesajul criptat prin XOR a fost recuperat folosind cheia 42, rezultatul fiind `SALUT`.
- Atacul de dicționar a identificat parola de test `moldova`, folosind algoritmul MD5.

## 3. Partea B — Analiza fișierelor

În fișierul `forensics.py` au fost implementate operații pentru identificarea tipurilor de fișiere, citirea metadatelor EXIF, detectarea unei arhive ZIP ascunse într-un PNG și extragerea conținutului acesteia.

Fotografia de test nu conține metadate EXIF sau coordonate GPS. Imaginea PNG conține o arhivă ZIP din care a fost extras fișierul `mesaj_secret.txt`.

Mesajul extras este: `Acesta este mesajul ascuns.`

## 4. Steganografie LSB

În fișierul `stego.py` au fost implementate funcții pentru ascunderea și extragerea unui mesaj folosind bitul cel mai puțin semnificativ (LSB) al componentelor RGB ale pixelilor.

Testul efectuat a confirmat recuperarea mesajului ascuns din imaginea generată.

## 5. Testare

Testul automat pentru decodificarea Base64 a trecut cu succes. Funcțiile XOR și verificarea hashurilor au fost testate pe fișierele generate pentru laborator.

## 6. Concluzie

În urma lucrării am înțeles cum pot fi analizate fișierele, cum pot fi recuperate date din codificări și cum pot fi detectate informații ascunse într-o imagine. Am exersat utilizarea Python pentru analiza fișierelor și verificarea rezultatelor prin teste.