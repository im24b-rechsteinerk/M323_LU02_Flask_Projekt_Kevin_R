import re

from app import app
from logic import Note

NOTEN = [
    Note("Mathematik", "Erste", 4.0, 2.0, 1, "2026-03-01"),
    Note("Biologie", "Zweite", 6.0, 1.0, 1, "2026-05-01"),
    Note("Mathematik", "Dritte", 5.0, 1.0, 2, "2026-01-01"),
]


def seite(monkeypatch, adresse):
    monkeypatch.setattr("app.load_noten", lambda: NOTEN)
    antwort = app.test_client().get(adresse)
    assert antwort.status_code == 200
    return antwort.get_data(as_text=True)


def pruefungen(html):
    return re.findall(r"<td>(Erste|Zweite|Dritte)</td>", html)


def loesch_indizes(html):
    return re.findall(r'action="/loeschen/(\d+)"', html)


def test_ohne_auswahl_zeigt_alle_wie_erfasst(monkeypatch):
    html = seite(monkeypatch, "/noten")
    assert pruefungen(html) == ["Erste", "Zweite", "Dritte"]
    assert loesch_indizes(html) == ["0", "1", "2"]


def test_filter_zeigt_nur_das_fach(monkeypatch):
    html = seite(monkeypatch, "/noten?fach=Mathematik")
    assert pruefungen(html) == ["Erste", "Dritte"]


def test_filter_berechnet_schnitt_und_gewicht_der_auswahl(monkeypatch):
    html = seite(monkeypatch, "/noten?fach=Mathematik")
    assert "4.33" in html
    assert "Gesamtgewicht: 3.0" in html


def test_sortierung_nach_note(monkeypatch):
    html = seite(monkeypatch, "/noten?sortierung=note")
    assert pruefungen(html) == ["Zweite", "Dritte", "Erste"]


def test_loeschen_behaelt_originalen_index_bei_filter_und_sortierung(monkeypatch):
    html = seite(monkeypatch, "/noten?fach=Mathematik&sortierung=datum")
    assert pruefungen(html) == ["Dritte", "Erste"]
    assert loesch_indizes(html) == ["2", "0"]


def test_loeschen_aus_gefilterter_liste_trifft_die_richtige_note(monkeypatch):
    gespeichert = []
    monkeypatch.setattr("app.load_noten", lambda: NOTEN)
    monkeypatch.setattr("app.save_noten", gespeichert.extend)
    html = app.test_client().get("/noten?fach=Biologie").get_data(as_text=True)
    index = loesch_indizes(html)[0]
    app.test_client().post(f"/loeschen/{index}")
    assert gespeichert == [NOTEN[0], NOTEN[2]]


def test_unbekanntes_fach_zeigt_keine_zeilen(monkeypatch):
    html = seite(monkeypatch, "/noten?fach=Physik")
    assert pruefungen(html) == []
    assert "Gesamtgewicht: 0.0" in html


def test_auswahl_bleibt_im_formular_erhalten(monkeypatch):
    html = seite(monkeypatch, "/noten?fach=Biologie&sortierung=note")
    assert '<option value="Biologie" selected>' in html
    assert '<option value="note" selected>' in html
