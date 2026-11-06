import pytest

from app import app
from logic import Note, note_aus_formular

GUELTIG = {
    "fach": " Physik ",
    "pruefung": "Test 1",
    "note": "4.5",
    "gewicht": "2",
    "semester": "1",
    "datum": "2026-11-06",
}


def test_gueltiges_formular_ergibt_note():
    assert note_aus_formular(GUELTIG) == (Note("Physik", "Test 1", 4.5, 2.0, 1, "2026-11-06"), [])


@pytest.mark.parametrize(
    ("feld", "wert", "meldung"),
    [
        ("fach", "   ", "Das Fach fehlt."),
        ("pruefung", "", "Die Prüfung fehlt."),
        ("note", "abc", "Die Note muss zwischen 1 und 6 liegen."),
        ("note", "7", "Die Note muss zwischen 1 und 6 liegen."),
        ("note", "0.9", "Die Note muss zwischen 1 und 6 liegen."),
        ("note", "nan", "Die Note muss zwischen 1 und 6 liegen."),
        ("gewicht", "0", "Das Gewicht muss grösser als 0 sein."),
        ("gewicht", "-1", "Das Gewicht muss grösser als 0 sein."),
        ("gewicht", "inf", "Das Gewicht muss grösser als 0 sein."),
        ("semester", "1.5", "Das Semester muss eine ganze Zahl ab 1 sein."),
        ("semester", "0", "Das Semester muss eine ganze Zahl ab 1 sein."),
        ("datum", "kein-datum", "Das Datum ist ungültig."),
        ("datum", "2026-02-30", "Das Datum ist ungültig."),
    ],
)
def test_ungueltiges_feld_ergibt_meldung(feld, wert, meldung):
    assert note_aus_formular({**GUELTIG, feld: wert}) == (None, [meldung])


@pytest.mark.parametrize("note", ["1", "6"])
def test_grenzen_der_note_sind_gueltig(note):
    neue, fehler = note_aus_formular({**GUELTIG, "note": note})
    assert fehler == []
    assert neue.note == float(note)


def test_fehlende_felder_ergeben_alle_meldungen():
    neue, fehler = note_aus_formular({})
    assert neue is None
    assert len(fehler) == 6


def test_route_speichert_gueltige_note(monkeypatch):
    gespeichert = []
    monkeypatch.setattr("app.load_noten", lambda: [])
    monkeypatch.setattr("app.save_noten", gespeichert.extend)
    antwort = app.test_client().post("/erfassen", data=GUELTIG)
    assert antwort.status_code == 302
    assert gespeichert == [Note("Physik", "Test 1", 4.5, 2.0, 1, "2026-11-06")]


def test_route_speichert_ungueltige_note_nicht(monkeypatch):
    gespeichert = []
    monkeypatch.setattr("app.load_noten", lambda: [])
    monkeypatch.setattr("app.save_noten", gespeichert.extend)
    antwort = app.test_client().post("/erfassen", data={**GUELTIG, "note": "7"})
    html = antwort.get_data(as_text=True)
    assert antwort.status_code == 400
    assert gespeichert == []
    assert "Die Note muss zwischen 1 und 6 liegen." in html
    assert 'value="Test 1"' in html
