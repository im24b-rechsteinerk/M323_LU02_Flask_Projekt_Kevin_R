from dataclasses import FrozenInstanceError

import pytest

from logic import (
    FachSchnitt,
    Note,
    fach_schnitt,
    faecher,
    faecher_ranking,
    gewichteter_durchschnitt,
    hinzufuegen,
    hinzufuegen_mutierend,
    nach_fach,
    note_delete,
    ranking_schluessel,
)


def beispiel(fach="Mathematik", note=5.0, gewicht=1.0):
    return Note(
        fach=fach,
        pruefung="Prüfung",
        note=note,
        gewicht=gewicht,
        semester=1,
        datum="2026-01-15",
    )


def test_note_ist_immutable():
    eintrag = beispiel()
    with pytest.raises(FrozenInstanceError):
        eintrag.note = 6.0


def test_hinzufuegen_haengt_neue_note_an():
    alt = beispiel(note=4.0)
    neu = beispiel(note=5.0)
    assert hinzufuegen([alt], neu) == [alt, neu]


def test_hinzufuegen_veraendert_original_nicht():
    noten = [beispiel()]
    hinzufuegen(noten, beispiel(note=4.0))
    assert len(noten) == 1


def test_hinzufuegen_mutierend_veraendert_original():
    noten = [beispiel()]
    resultat = hinzufuegen_mutierend(noten, beispiel(note=4.0))
    assert resultat is noten
    assert len(noten) == 2


def test_durchschnitt_beruecksichtigt_gewicht():
    noten = [beispiel(note=4.0, gewicht=2.0), beispiel(note=5.5, gewicht=1.0)]
    assert gewichteter_durchschnitt(noten) == pytest.approx(4.5)


def test_durchschnitt_einer_einzelnen_note():
    assert gewichteter_durchschnitt([beispiel(note=3.5, gewicht=0.5)]) == pytest.approx(3.5)


def test_durchschnitt_ohne_noten_ist_none():
    assert gewichteter_durchschnitt([]) is None


def test_durchschnitt_mit_gewicht_null_ist_none():
    assert gewichteter_durchschnitt([beispiel(gewicht=0.0)]) is None


def test_faecher_sortiert_ohne_duplikate():
    noten = [beispiel("Mathematik"), beispiel("Englisch"), beispiel("Mathematik")]
    assert faecher(noten) == ["Englisch", "Mathematik"]


def test_faecher_ohne_noten_ist_leer():
    assert faecher([]) == []


def test_note_delete_entfernt_nur_den_index():
    erste, zweite, dritte = beispiel(note=4.0), beispiel(note=5.0), beispiel(note=6.0)
    assert note_delete([erste, zweite, dritte], 1) == [erste, dritte]


def test_note_delete_veraendert_original_nicht():
    noten = [beispiel(note=4.0), beispiel(note=5.0)]
    note_delete(noten, 0)
    assert len(noten) == 2


def test_nach_fach_gruppiert_und_behaelt_reihenfolge():
    erste, zweite = beispiel("Mathematik", note=4.0), beispiel("Mathematik", note=5.0)
    englisch = beispiel("Englisch")
    assert nach_fach([erste, englisch, zweite]) == {
        "Englisch": [englisch],
        "Mathematik": [erste, zweite],
    }


def test_nach_fach_ohne_noten_ist_leer():
    assert nach_fach([]) == {}


def test_fach_schnitt_berechnet_schnitt_und_anzahl():
    noten = [beispiel(note=4.0, gewicht=2.0), beispiel(note=5.5, gewicht=1.0)]
    assert fach_schnitt("Mathematik", noten) == FachSchnitt("Mathematik", 4.5, 2)


def test_fach_schnitt_mit_gewicht_null_ist_none():
    assert fach_schnitt("Mathematik", [beispiel(gewicht=0.0)]) is None


def test_ranking_schluessel_sortiert_besten_schnitt_nach_vorne():
    besser = FachSchnitt("Chemie", 5.0, 1)
    schlechter = FachSchnitt("Biologie", 4.0, 1)
    assert sorted([schlechter, besser], key=ranking_schluessel) == [besser, schlechter]


def test_ranking_schluessel_sortiert_gleichstand_alphabetisch():
    biologie = FachSchnitt("Biologie", 5.0, 1)
    chemie = FachSchnitt("Chemie", 5.0, 1)
    assert sorted([chemie, biologie], key=ranking_schluessel) == [biologie, chemie]


def test_faecher_ranking_setzt_alle_schritte_zusammen():
    noten = [
        beispiel("Chemie", note=4.0),
        beispiel("Biologie", note=5.0, gewicht=0.0),
        beispiel("Physik", note=5.0),
    ]
    assert faecher_ranking(noten) == [
        FachSchnitt("Physik", 5.0, 1),
        FachSchnitt("Chemie", 4.0, 1),
    ]


def test_faecher_ranking_ohne_noten_ist_leer():
    assert faecher_ranking([]) == []


def test_faecher_ranking_veraendert_eingabe_nicht():
    noten = [beispiel("Chemie"), beispiel("Biologie")]
    kopie = list(noten)
    faecher_ranking(noten)
    assert noten == kopie
