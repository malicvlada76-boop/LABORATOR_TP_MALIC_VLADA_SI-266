
from PIL import Image


# B5. Ascundem mesajul în ultimii biți ai pixelilor.
def ascunde_mesaj():
    img = Image.open("probe/foto.jpg").convert("RGB")
    px = list(img.getdata())

    mesaj = b"FLAG{ascuns_in_pixeli}\0"
    biti = "".join(f"{x:08b}" for x in mesaj)

    if len(biti) > len(px) * 3:
        raise ValueError("Mesajul este prea lung pentru imagine!")

    px_nou = []
    index = 0

    for r, g, b in px:
        canale = [r, g, b]

        for i in range(3):
            if index < len(biti):
                canale[i] = (
                    (canale[i] & ~1) | int(biti[index])
                )
                index += 1

        px_nou.append(tuple(canale))

    img.putdata(px_nou)
    img.save("stego.png", format="PNG")

    print("Mesajul a fost ascuns în stego.png")


# B6. Extragem mesajul din ultimii biți ai pixelilor.
def dezvaluie_mesaj():
    px = list(Image.open("stego.png").convert("RGB").getdata())

    biti = ""

    for r, g, b in px:
        biti += str(r & 1)
        biti += str(g & 1)
        biti += str(b & 1)

    rezultat = bytearray()

    for i in range(0, len(biti) - 7, 8):
        octet = biti[i:i + 8]
        valoare = int(octet, 2)

        if valoare == 0:
            break

        rezultat.append(valoare)

    mesaj = rezultat.decode("utf-8")
    print("Mesajul recuperat:", mesaj)

    return mesaj


if __name__ == "__main__":
    ascunde_mesaj()
    dezvaluie_mesaj()
