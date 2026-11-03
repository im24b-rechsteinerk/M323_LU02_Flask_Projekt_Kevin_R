from app import app
from logic import Note


def beispiel(fach, note, gewicht=1.0):
    return Note(
        fach=fach,
        pruefung="Prüfung",
        note=note,
        gewicht=gewicht,
        semester=1,
        datum="2026-01-15",
    )


def ziel_seite(monkeypatch, noten, adresse):
    monkeypatch.setattr("app.load_noten", lambda: noten)
    antwort = app.test_client().get(adresse)
    assert antwort.status_code == 200
    return antwort.get_data(as_text=True)


def test_ohne_auswahl_zeigt_formular_ohne_ergebnis(monkeypatch):
    seite = ziel_seite(monkeypatch, [beispiel("Physik", 4.0)], "/ziel")
    assert '<option value="Physik"' in seite
    assert 'class="ergebnis"' not in seite


def test_ohne_noten_zeigt_hinweis(monkeypatch):
    assert "Noch keine Noten erfasst" in ziel_seite(monkeypatch, [], "/ziel")


def test_zeigt_benoetigte_note(monkeypatch):
    seite = ziel_seite(monkeypatch, [beispiel("Physik", 3.5)], "/ziel?fach=Physik&gewicht=1")
    assert "mindestens eine 4.50" in seite


def test_zeigt_wenn_jede_note_reicht(monkeypatch):
    seite = ziel_seite(monkeypatch, [beispiel("Physik", 6.0, 3.0)], "/ziel?fach=Physik&gewicht=1")
    assert "mit jeder Note" in seite


def test_zeigt_wenn_ziel_nicht_erreichbar(monkeypatch):
    seite = ziel_seite(monkeypatch, [beispiel("Physik", 2.0, 3.0)], "/ziel?fach=Physik&gewicht=1")
    assert "nicht erreichbar" in seite


def test_zeigt_fehler_bei_gewicht_null(monkeypatch):
    seite = ziel_seite(monkeypatch, [beispiel("Physik", 4.0)], "/ziel?fach=Physik&gewicht=0")
    assert "grösser als 0" in seite


def test_ungueltiges_gewicht_nutzt_standardwert(monkeypatch):
    seite = ziel_seite(monkeypatch, [beispiel("Physik", 3.5)], "/ziel?fach=Physik&gewicht=abc")
    assert "mindestens eine 4.50" in seite


def test_gewaehltes_fach_bleibt_ausgewaehlt(monkeypatch):
    noten = [beispiel("Biologie", 4.0), beispiel("Physik", 4.0)]
    seite = ziel_seite(monkeypatch, noten, "/ziel?fach=Physik&gewicht=1")
    assert '<option value="Physik" selected>' in seite
