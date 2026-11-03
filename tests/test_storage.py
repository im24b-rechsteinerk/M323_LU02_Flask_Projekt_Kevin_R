from logic import Note
from storage import load_noten, save_noten


def beispiel():
    return Note(
        fach="Mathematik",
        pruefung="Abschlussprüfung, Teil 1",
        note=4.5,
        gewicht=2.0,
        semester=1,
        datum="2026-06-20",
    )


def test_speichern_und_laden_ergibt_dieselben_noten(tmp_path):
    pfad = tmp_path / "noten.csv"
    save_noten([beispiel()], pfad)
    assert load_noten(pfad) == [beispiel()]


def test_laden_wandelt_zahlen_um(tmp_path):
    pfad = tmp_path / "noten.csv"
    pfad.write_text(
        "fach,pruefung,note,gewicht,semester,datum\n"
        "Englisch,Essay,4.5,1.0,2,2026-04-18\n",
        encoding="utf-8",
    )
    eintrag = load_noten(pfad)[0]
    assert eintrag.note == 4.5
    assert eintrag.gewicht == 1.0
    assert eintrag.semester == 2


def test_laden_ohne_datei_ist_leer(tmp_path):
    assert load_noten(tmp_path / "fehlt.csv") == []


def test_leere_liste_speichert_nur_kopfzeile(tmp_path):
    pfad = tmp_path / "noten.csv"
    save_noten([], pfad)
    assert pfad.read_text(encoding="utf-8").strip() == "fach,pruefung,note,gewicht,semester,datum"
    assert load_noten(pfad) == []


def test_speichern_ueberschreibt_alte_daten(tmp_path):
    pfad = tmp_path / "noten.csv"
    save_noten([beispiel(), beispiel()], pfad)
    save_noten([beispiel()], pfad)
    assert len(load_noten(pfad)) == 1
