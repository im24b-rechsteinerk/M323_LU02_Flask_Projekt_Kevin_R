"""Tests fuer den funktionalen Kern der Notenliste - ohne Flask und ohne Server."""

from logic import Note, NotenZeile, notenliste_ansicht

NOTEN = [
    Note("Mathematik", "Erste", 4.0, 2.0, 1, "2026-03-01"),
    Note("Biologie", "Zweite", 6.0, 1.0, 1, "2026-05-01"),
    Note("Mathematik", "Dritte", 5.0, 1.0, 2, "2026-01-01"),
]


def test_ansicht_filtert_sortiert_und_rechnet():
    ansicht = notenliste_ansicht(NOTEN, "Mathematik", "note")
    assert ansicht["zeilen"] == [NotenZeile(2, NOTEN[2]), NotenZeile(0, NOTEN[0])]
    assert round(ansicht["schnitt"], 2) == 4.33
    assert ansicht["gesamtgewicht"] == 3.0
    assert ansicht["faecher"] == ["Biologie", "Mathematik"]


def test_ansicht_ohne_noten_hat_keinen_schnitt():
    ansicht = notenliste_ansicht([], "", "erfasst")
    assert ansicht["zeilen"] == []
    assert ansicht["schnitt"] is None
    assert ansicht["gesamtgewicht"] == 0.0


def test_ansicht_veraendert_eingabe_nicht():
    noten = list(NOTEN)
    notenliste_ansicht(noten, "", "datum")
    assert noten == NOTEN


def test_ansicht_ist_deterministisch():
    assert notenliste_ansicht(NOTEN, "", "fach") == notenliste_ansicht(NOTEN, "", "fach")
