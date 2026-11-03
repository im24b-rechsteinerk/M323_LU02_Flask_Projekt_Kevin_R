"""Misst die Laufzeit der Route /ranking mit künstlichen Daten."""

import timeit

import app as app_modul
from logic import Note

GROESSEN = ((1_000, 10), (10_000, 50), (10_000, 500))


def testdaten(anzahl_noten, anzahl_faecher):
    return [
        Note(
            fach=f"Fach {i % anzahl_faecher}",
            pruefung=f"Prüfung {i}",
            note=1 + i % 51 / 10,
            gewicht=1.0 + i % 3,
            semester=1 + i % 2,
            datum="2026-01-15",
        )
        for i in range(anzahl_noten)
    ]


def messen(noten):
    app_modul.load_noten = lambda: noten
    client = app_modul.app.test_client()
    zeiten = timeit.repeat(lambda: client.get("/ranking"), repeat=5, number=1)
    return min(zeiten) * 1000


if __name__ == "__main__":
    print("Noten | Fächer | beste Zeit von 5 Läufen")
    for anzahl_noten, anzahl_faecher in GROESSEN:
        dauer = messen(testdaten(anzahl_noten, anzahl_faecher))
        print(f"{anzahl_noten} | {anzahl_faecher} | {dauer:.1f} ms")
