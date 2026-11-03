import re

from app import app
from logic import Note

ZEILE = re.compile(
    r"<tr>\s*" + r"\s*".join([r"<td>([^<]*)</td>"] * 6)
)


def beispiel(semester, note, gewicht=1.0):
    return Note(
        fach="Mathematik",
        pruefung="Prüfung",
        note=note,
        gewicht=gewicht,
        semester=semester,
        datum="2026-01-15",
    )


def semester_seite(monkeypatch, noten):
    monkeypatch.setattr("app.load_noten", lambda: noten)
    antwort = app.test_client().get("/semester")
    assert antwort.status_code == 200
    return antwort.get_data(as_text=True)


def test_semester_mit_gewichten_und_ungenuegenden_noten(monkeypatch):
    noten = [
        beispiel(2, 5.5),
        beispiel(2, 3.5),
        beispiel(2, 4.0, 0.5),
        beispiel(2, 5.0, 2.0),
        beispiel(2, 3.5),
        beispiel(1, 4.5),
        beispiel(1, 4.0, 2.0),
    ]
    assert ZEILE.findall(semester_seite(monkeypatch, noten)) == [
        ("1", "4.17", "2", "0", "0.0", "4.5"),
        ("2", "4.45", "5", "2", "1.0", "5.5"),
    ]


def test_ohne_noten_zeigt_hinweis(monkeypatch):
    seite = semester_seite(monkeypatch, [])
    assert ZEILE.findall(seite) == []
    assert "Noch keine Noten" in seite


def test_semester_mit_gewicht_null_zeigt_keinen_schnitt(monkeypatch):
    assert ZEILE.findall(semester_seite(monkeypatch, [beispiel(1, 5.0, 0.0)])) == [
        ("1", "–", "1", "0", "0.0", "5.0"),
    ]
