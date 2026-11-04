import pytest

from logic import Note, gewichteter_durchschnitt, hinzufuegen
from paradigmen import Notenbuch, durchschnitt_prozedural


def beispiel(note, gewicht=1.0):
    return Note(
        fach="Mathematik",
        pruefung="Prüfung",
        note=note,
        gewicht=gewicht,
        semester=1,
        datum="2026-01-15",
    )


def durchschnitt_oo(noten):
    return Notenbuch(noten).durchschnitt()


VARIANTEN = [durchschnitt_prozedural, durchschnitt_oo, gewichteter_durchschnitt]


@pytest.mark.parametrize("variante", VARIANTEN)
def test_alle_varianten_rechnen_gleich(variante):
    noten = [beispiel(4.0, 2.0), beispiel(5.5, 1.0)]
    assert variante(noten) == pytest.approx(4.5)


@pytest.mark.parametrize("variante", VARIANTEN)
def test_alle_varianten_ohne_noten_sind_none(variante):
    assert variante([]) is None


@pytest.mark.parametrize("variante", VARIANTEN)
def test_alle_varianten_mit_gewicht_null_sind_none(variante):
    assert variante([beispiel(5.0, 0.0)]) is None


def test_oo_gleicher_aufruf_liefert_nach_aenderung_anderes_ergebnis():
    notenbuch = Notenbuch([beispiel(4.0)])
    vorher = notenbuch.durchschnitt()
    notenbuch.hinzufuegen(beispiel(6.0))
    assert vorher == pytest.approx(4.0)
    assert notenbuch.durchschnitt() == pytest.approx(5.0)


def test_funktional_gleicher_aufruf_liefert_immer_dasselbe_ergebnis():
    noten = [beispiel(4.0)]
    vorher = gewichteter_durchschnitt(noten)
    neu = hinzufuegen(noten, beispiel(6.0))
    assert gewichteter_durchschnitt(noten) == vorher
    assert gewichteter_durchschnitt(neu) == pytest.approx(5.0)
