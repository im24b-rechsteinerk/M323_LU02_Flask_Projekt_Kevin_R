"""Misst semester_statistiken vorher (pro Semester alle Noten filtern) und nachher (einmal gruppieren)."""

import timeit

import app as app_modul
from logic import Note, semester_liste, semester_statistik, semester_statistiken

GROESSEN = ((100, 8), (1_000, 8), (10_000, 8), (100_000, 8))


def testdaten(anzahl_noten, anzahl_semester):
    return [
        Note(
            fach=f"Fach {i % 12}",
            pruefung=f"Prüfung {i}",
            note=1 + i % 51 / 10,
            gewicht=1.0 + i % 3,
            semester=1 + i % anzahl_semester,
            datum="2026-01-15",
        )
        for i in range(anzahl_noten)
    ]


def vorher(noten):
    """Ursprüngliche Fassung: für jedes Semester werden alle Noten durchsucht."""
    return list(map(lambda semester: semester_statistik(noten, semester), semester_liste(noten)))


def beste_zeit_ms(funktion, noten):
    return min(timeit.repeat(lambda: funktion(noten), repeat=5, number=1)) * 1000


def route_ms(noten):
    app_modul.load_noten = lambda: noten
    client = app_modul.app.test_client()
    return min(timeit.repeat(lambda: client.get("/semester"), repeat=5, number=1)) * 1000


if __name__ == "__main__":
    print("Noten | Semester | vorher | nachher | Faktor")
    for anzahl_noten, anzahl_semester in GROESSEN:
        noten = testdaten(anzahl_noten, anzahl_semester)
        assert vorher(noten) == semester_statistiken(noten)
        alt = beste_zeit_ms(vorher, noten)
        neu = beste_zeit_ms(semester_statistiken, noten)
        print(f"{anzahl_noten} | {anzahl_semester} | {alt:.2f} ms | {neu:.2f} ms | {alt / neu:.1f}")
    print(f"Route /semester mit 10000 Noten, 8 Semestern: {route_ms(testdaten(10_000, 8)):.2f} ms")
