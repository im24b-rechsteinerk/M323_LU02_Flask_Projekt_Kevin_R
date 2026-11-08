"""Characterization Tests vor dem Refactoring der Routen (LU07.A12).

Diese Tests halten fest, was /noten und /erfassen heute tun - inklusive
Statuscode und der entscheidenden Inhalte der Response. Sie wurden vor dem
Umbau geschrieben und muessen nach jedem Refactoring-Schritt gruen bleiben.
"""

import re

from app import app
from logic import Note

NOTEN = [
    Note("Mathematik", "Erste", 4.0, 2.0, 1, "2026-03-01"),
    Note("Biologie", "Zweite", 6.0, 1.0, 1, "2026-05-01"),
    Note("Mathematik", "Dritte", 5.0, 1.0, 2, "2026-01-01"),
]

GUELTIG = {
    "fach": "Physik",
    "pruefung": "Test 1",
    "note": "4.5",
    "gewicht": "2",
    "semester": "1",
    "datum": "2026-11-06",
}


def client_mit(monkeypatch, noten, gespeichert=None):
    monkeypatch.setattr("app.load_noten", lambda: noten)
    if gespeichert is not None:
        monkeypatch.setattr("app.save_noten", gespeichert.extend)
    return app.test_client()


def pruefungen(html):
    return re.findall(r"<td>(Erste|Zweite|Dritte)</td>", html)


def test_noten_zeigt_schnitt_und_gesamtgewicht_aller_noten(monkeypatch):
    antwort = client_mit(monkeypatch, NOTEN).get("/noten")
    html = antwort.get_data(as_text=True)
    assert antwort.status_code == 200
    assert "4.75" in html
    assert "Gesamtgewicht: 4.0" in html


def test_noten_unbekannte_sortierung_bleibt_wie_erfasst(monkeypatch):
    antwort = client_mit(monkeypatch, NOTEN).get("/noten?sortierung=quatsch")
    assert antwort.status_code == 200
    assert pruefungen(antwort.get_data(as_text=True)) == ["Erste", "Zweite", "Dritte"]


def test_noten_ohne_noten_zeigt_strich_statt_schnitt(monkeypatch):
    antwort = client_mit(monkeypatch, []).get("/noten")
    html = antwort.get_data(as_text=True)
    assert antwort.status_code == 200
    assert re.search(r"Gewichteter Durchschnitt:\s*–\s*· Gesamtgewicht: 0.0", html)


def test_erfassen_get_zeigt_leeres_formular_mit_faechern(monkeypatch):
    antwort = client_mit(monkeypatch, NOTEN).get("/erfassen")
    html = antwort.get_data(as_text=True)
    assert antwort.status_code == 200
    assert '<ul class="fehler">' not in html
    assert '<option value="Biologie"></option>' in html
    assert '<option value="Mathematik"></option>' in html
    assert 'name="pruefung" value=""' in html


def test_erfassen_head_verhaelt_sich_wie_get(monkeypatch):
    antwort = client_mit(monkeypatch, NOTEN).head("/erfassen")
    assert antwort.status_code == 200


def test_erfassen_ungueltig_gibt_400_mit_faechern_und_eingaben(monkeypatch):
    gespeichert = []
    antwort = client_mit(monkeypatch, NOTEN, gespeichert).post("/erfassen", data={**GUELTIG, "fach": ""})
    html = antwort.get_data(as_text=True)
    assert antwort.status_code == 400
    assert "Das Fach fehlt." in html
    assert '<option value="Mathematik"></option>' in html
    assert 'value="Test 1"' in html
    assert gespeichert == []


def test_erfassen_gueltig_speichert_leitet_weiter_und_meldet(monkeypatch):
    gespeichert = []
    antwort = client_mit(monkeypatch, NOTEN, gespeichert).post("/erfassen", data=GUELTIG, follow_redirects=True)
    assert antwort.status_code == 200
    assert antwort.request.path == "/noten"
    assert "Note gespeichert." in antwort.get_data(as_text=True)
    assert gespeichert == [*NOTEN, Note("Physik", "Test 1", 4.5, 2.0, 1, "2026-11-06")]
