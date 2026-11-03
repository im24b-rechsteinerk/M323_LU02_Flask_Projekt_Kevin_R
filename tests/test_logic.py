from dataclasses import FrozenInstanceError

import pytest

from logic import (
    Note,
    faecher,
    gewichteter_durchschnitt,
    hinzufuegen,
    hinzufuegen_mutierend,
    note_delete,
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
