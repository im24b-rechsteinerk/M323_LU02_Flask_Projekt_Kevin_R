import re

from app import app
from logic import Note

ZEILE = re.compile(
    r"<tr[^>]*>\s*<td>(\d+)</td>\s*<td>([^<]*)</td>\s*<td>([^<]*)</td>\s*<td>(\d+)</td>"
)


def beispiel(fach, note, gewicht=1.0):
    return Note(
        fach=fach,
        pruefung="Prüfung",
        note=note,
        gewicht=gewicht,
        semester=1,
        datum="2026-01-15",
    )


def ranking_zeilen(monkeypatch, noten):
    monkeypatch.setattr("app.load_noten", lambda: noten)
    antwort = app.test_client().get("/ranking")
    assert antwort.status_code == 200
    return ZEILE.findall(antwort.get_data(as_text=True))


def test_ranking_mit_daten_aus_dem_design_blatt(monkeypatch):
    noten = [
        beispiel("Mathematik", 4.5),
        beispiel("Mathematik", 4.0, 2.0),
        beispiel("Englisch", 5.5, 0.5),
        beispiel("Englisch", 4.5),
        beispiel("Englisch", 5.0),
        beispiel("Informatik", 5.5),
        beispiel("Informatik", 4.0),
        beispiel("Mathematik", 5.5),
        beispiel("Mathematik", 3.5),
        beispiel("Englisch", 4.0, 0.5),
        beispiel("Informatik", 5.0, 2.0),
        beispiel("Wirtschaft", 4.5),
        beispiel("Wirtschaft", 3.5),
    ]
    assert ranking_zeilen(monkeypatch, noten) == [
        ("1", "Informatik", "4.88", "3"),
        ("2", "Englisch", "4.75", "4"),
        ("3", "Mathematik", "4.30", "4"),
        ("4", "Wirtschaft", "4.00", "2"),
    ]


def test_ranking_ohne_noten_ist_leer(monkeypatch):
    assert ranking_zeilen(monkeypatch, []) == []


def test_ranking_ohne_noten_zeigt_hinweis(monkeypatch):
    monkeypatch.setattr("app.load_noten", lambda: [])
    antwort = app.test_client().get("/ranking")
    assert "Noch keine Noten" in antwort.get_data(as_text=True)


def test_fach_mit_gewicht_null_fehlt_im_ranking(monkeypatch):
    noten = [beispiel("Biologie", 5.0, 0.0), beispiel("Chemie", 4.0)]
    assert ranking_zeilen(monkeypatch, noten) == [("1", "Chemie", "4.00", "1")]


def test_gleichstand_ist_alphabetisch_sortiert(monkeypatch):
    noten = [beispiel("Chemie", 5.0), beispiel("Biologie", 5.0)]
    assert ranking_zeilen(monkeypatch, noten) == [
        ("1", "Biologie", "5.00", "1"),
        ("2", "Chemie", "5.00", "1"),
    ]


def test_schnitt_beruecksichtigt_gewicht(monkeypatch):
    noten = [beispiel("Physik", 4.0, 2.0), beispiel("Physik", 5.5, 1.0)]
    assert ranking_zeilen(monkeypatch, noten) == [("1", "Physik", "4.50", "2")]


def test_ranking_veraendert_eingabe_nicht(monkeypatch):
    noten = [beispiel("Chemie", 4.0), beispiel("Biologie", 5.0)]
    kopie = list(noten)
    ranking_zeilen(monkeypatch, noten)
    assert noten == kopie
