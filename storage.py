"""CSV lesen und schreiben – einzige Stelle mit I/O."""

import csv
from pathlib import Path

from logic import Note

FELDER = ("fach", "pruefung", "note", "gewicht", "semester", "datum")
CSV_PFAD = Path(__file__).parent / "data" / "noten.csv"


def load_noten(path=CSV_PFAD):
    path = Path(path)
    if not path.exists():
        return []

    with path.open(encoding="utf-8", newline="") as datei:
        reader = csv.DictReader(datei)
        return [
            Note(
                fach=zeile["fach"],
                pruefung=zeile["pruefung"],
                note=float(zeile["note"]),
                gewicht=float(zeile["gewicht"]),
                semester=int(zeile["semester"]),
                datum=zeile["datum"],
            )
            for zeile in reader
        ]


def save_noten(noten, path=CSV_PFAD):
    path = Path(path)
    with path.open("w", encoding="utf-8", newline="") as datei:
        writer = csv.DictWriter(datei, fieldnames=FELDER)
        writer.writeheader()
        for eintrag in noten:
            writer.writerow(
                {
                    "fach": eintrag.fach,
                    "pruefung": eintrag.pruefung,
                    "note": eintrag.note,
                    "gewicht": eintrag.gewicht,
                    "semester": eintrag.semester,
                    "datum": eintrag.datum,
                }
            )
