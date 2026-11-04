from dataclasses import FrozenInstanceError

import pytest

from logic import (
    FachSchnitt,
    Note,
    NotenZeile,
    SemesterStatistik,
    abstand_zu_genuegend,
    fach_schnitt,
    faecher,
    faecher_ranking,
    benoetigte_note,
    gesamtgewicht,
    gewichtete_punkte,
    gewichteter_durchschnitt,
    hinzufuegen,
    hinzufuegen_mutierend,
    nach_fach,
    note_delete,
    noten_von_fach,
    noten_zeilen,
    ranking_schluessel,
    semester_liste,
    semester_statistik,
    semester_statistiken,
    sortieren,
    summe_gewichte,
    ungenuegende_noten,
    zeilen_von_fach,
    ziel_berechnen,
    ziel_status,
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


def test_noten_von_fach_filtert_nach_fach():
    mathe, englisch = beispiel("Mathematik"), beispiel("Englisch")
    assert noten_von_fach([mathe, englisch], "Englisch") == [englisch]


def test_gewichtete_punkte_und_summe_gewichte():
    noten = [beispiel(note=4.0, gewicht=2.0), beispiel(note=5.5, gewicht=1.0)]
    assert gewichtete_punkte(noten) == pytest.approx(13.5)
    assert summe_gewichte(noten) == pytest.approx(3.0)


def test_punkte_und_gewichte_ohne_noten_sind_null():
    assert gewichtete_punkte([]) == 0
    assert summe_gewichte([]) == 0


def test_benoetigte_note_rechnet_mit_formel():
    assert benoetigte_note(21.5, 5.0, 1.0, 4.0) == pytest.approx(2.5)


def test_benoetigte_note_beruecksichtigt_neues_gewicht():
    assert benoetigte_note(21.5, 5.0, 2.0, 4.0) == pytest.approx(3.25)


@pytest.mark.parametrize(
    ("note", "status"),
    [
        (0.99, "sicher"),
        (1.0, "moeglich"),
        (4.0, "moeglich"),
        (6.0, "moeglich"),
        (6.01, "unmoeglich"),
    ],
)
def test_ziel_status_an_den_grenzen(note, status):
    assert ziel_status(note) == status


def test_ziel_berechnen_mit_mathematik_aus_echten_daten():
    noten = [
        beispiel("Mathematik", note=4.5),
        beispiel("Mathematik", note=4.0, gewicht=2.0),
        beispiel("Mathematik", note=5.5),
        beispiel("Mathematik", note=3.5),
        beispiel("Englisch", note=1.0),
    ]
    ergebnis = ziel_berechnen(noten, "Mathematik", 1.0)
    assert ergebnis.fach == "Mathematik"
    assert ergebnis.note == pytest.approx(2.5)
    assert ergebnis.status == "moeglich"


def test_ziel_berechnen_ohne_noten_braucht_das_ziel_selbst():
    assert ziel_berechnen([], "Mathematik", 1.0).note == pytest.approx(4.0)


def test_ziel_berechnen_schon_sicher():
    ergebnis = ziel_berechnen([beispiel(note=6.0, gewicht=3.0)], "Mathematik", 1.0)
    assert ergebnis.note == pytest.approx(-2.0)
    assert ergebnis.status == "sicher"


def test_ziel_berechnen_nicht_erreichbar():
    ergebnis = ziel_berechnen([beispiel(note=2.0, gewicht=3.0)], "Mathematik", 1.0)
    assert ergebnis.note == pytest.approx(10.0)
    assert ergebnis.status == "unmoeglich"


@pytest.mark.parametrize("gewicht", [0.0, -1.0, float("inf"), float("nan")])
def test_ziel_berechnen_mit_ungueltigem_gewicht_ist_none(gewicht):
    assert ziel_berechnen([beispiel()], "Mathematik", gewicht) is None


def im_semester(semester, note=5.0, gewicht=1.0):
    return Note(
        fach="Mathematik",
        pruefung="Prüfung",
        note=note,
        gewicht=gewicht,
        semester=semester,
        datum="2026-01-15",
    )


def test_semester_liste_sortiert_ohne_duplikate():
    noten = [im_semester(2), im_semester(1), im_semester(2)]
    assert semester_liste(noten) == [1, 2]


def test_ungenuegende_noten_zaehlt_die_4_nicht_mit():
    drei_fuenf, vier = im_semester(1, note=3.5), im_semester(1, note=4.0)
    assert ungenuegende_noten([drei_fuenf, vier]) == [drei_fuenf]


def test_abstand_zu_genuegend_summiert_nur_ungenuegende():
    noten = [im_semester(1, note=3.5), im_semester(1, note=2.0), im_semester(1, note=5.0)]
    assert abstand_zu_genuegend(noten) == pytest.approx(2.5)


def test_abstand_zu_genuegend_ohne_ungenuegende_ist_null():
    assert abstand_zu_genuegend([im_semester(1, note=5.0)]) == 0


def test_semester_statistik_berechnet_alle_werte():
    noten = [
        im_semester(1, note=4.0, gewicht=2.0),
        im_semester(1, note=5.5),
        im_semester(1, note=3.5),
        im_semester(2, note=6.0),
    ]
    statistik = semester_statistik(noten, 1)
    assert statistik.semester == 1
    assert statistik.schnitt == pytest.approx(4.25)
    assert statistik.anzahl == 3
    assert statistik.ungenuegend == 1
    assert statistik.abstand == pytest.approx(0.5)
    assert statistik.beste_note == 5.5


def test_semester_statistik_mit_gewicht_null_hat_keinen_schnitt():
    statistik = semester_statistik([im_semester(1, note=5.0, gewicht=0.0)], 1)
    assert statistik.schnitt is None
    assert statistik.anzahl == 1


def test_semester_statistik_ohne_noten_im_semester():
    assert semester_statistik([im_semester(2)], 1) == SemesterStatistik(1, None, 0, 0, 0.0, None)


def test_semester_statistiken_liefert_jedes_semester_in_reihenfolge():
    noten = [im_semester(2), im_semester(1)]
    assert [statistik.semester for statistik in semester_statistiken(noten)] == [1, 2]


def test_semester_statistiken_ohne_noten_ist_leer():
    assert semester_statistiken([]) == []


def test_semester_statistiken_veraendert_eingabe_nicht():
    noten = [im_semester(2), im_semester(1)]
    kopie = list(noten)
    semester_statistiken(noten)
    assert noten == kopie


def test_noten_zeilen_merkt_sich_den_index():
    erste, zweite = beispiel(note=4.0), beispiel(note=5.0)
    assert noten_zeilen([erste, zweite]) == [NotenZeile(0, erste), NotenZeile(1, zweite)]


def test_zeilen_von_fach_behaelt_den_originalen_index():
    zeilen = noten_zeilen([beispiel("Mathematik"), beispiel("Englisch")])
    assert zeilen_von_fach(zeilen, "Englisch") == [NotenZeile(1, beispiel("Englisch"))]


def test_zeilen_von_fach_ohne_fach_liefert_alle():
    zeilen = noten_zeilen([beispiel("Mathematik"), beispiel("Englisch")])
    assert zeilen_von_fach(zeilen, "") == zeilen


def test_zeilen_von_unbekanntem_fach_sind_leer():
    assert zeilen_von_fach(noten_zeilen([beispiel("Mathematik")]), "Physik") == []


def indizes_nach_sortierung(sortierung):
    zeilen = noten_zeilen(
        [
            Note("Mathematik", "A", 4.0, 1.0, 1, "2026-03-01"),
            Note("Biologie", "B", 6.0, 1.0, 1, "2026-05-01"),
            Note("Chemie", "C", 5.0, 1.0, 1, "2026-01-01"),
        ]
    )
    return [zeile.index for zeile in sortieren(zeilen, sortierung)]


@pytest.mark.parametrize(
    ("sortierung", "indizes"),
    [
        ("erfasst", [0, 1, 2]),
        ("datum", [2, 0, 1]),
        ("note", [1, 2, 0]),
        ("fach", [1, 2, 0]),
        ("unbekannt", [0, 1, 2]),
    ],
)
def test_sortieren_nach_jeder_sortierung(sortierung, indizes):
    assert indizes_nach_sortierung(sortierung) == indizes


def test_sortieren_veraendert_eingabe_nicht():
    zeilen = noten_zeilen([beispiel(note=4.0), beispiel(note=6.0)])
    kopie = list(zeilen)
    sortieren(zeilen, "note")
    assert zeilen == kopie


def test_gesamtgewicht_summiert_die_gewichte():
    zeilen = noten_zeilen([beispiel(gewicht=2.0), beispiel(gewicht=0.5)])
    assert gesamtgewicht(zeilen) == pytest.approx(2.5)


def test_gesamtgewicht_ohne_zeilen_ist_null():
    assert gesamtgewicht([]) == 0
