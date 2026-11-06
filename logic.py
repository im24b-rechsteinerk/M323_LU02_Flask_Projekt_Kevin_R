import math
from dataclasses import dataclass
from datetime import date
from functools import reduce
from itertools import groupby
from operator import attrgetter

NOTE_MIN = 1.0
NOTE_MAX = 6.0
NOTE_GENUEGEND = 4.0


@dataclass(frozen=True)
class Note:
    fach: str
    pruefung: str
    note: float
    gewicht: float
    semester: int
    datum: str


@dataclass(frozen=True)
class NotenZeile:
    index: int
    eintrag: Note


@dataclass(frozen=True)
class FachSchnitt:
    fach: str
    schnitt: float
    anzahl: int


@dataclass(frozen=True)
class Zielergebnis:
    fach: str
    note: float
    status: str


@dataclass(frozen=True)
class SemesterStatistik:
    semester: int
    schnitt: float | None
    anzahl: int
    ungenuegend: int
    abstand: float
    beste_note: float | None


def hinzufuegen(noten, neue):
    return [*noten, neue]


def hinzufuegen_mutierend(noten, neue):
    noten.append(neue)
    return noten


def gewichteter_durchschnitt(noten):
    if not noten:
        return None
    gewicht_summe = sum(eintrag.gewicht for eintrag in noten)
    if gewicht_summe == 0:
        return None
    return sum(eintrag.note * eintrag.gewicht for eintrag in noten) / gewicht_summe


def faecher(noten):
    return sorted({eintrag.fach for eintrag in noten})

def note_delete(noten, index):
    return noten[:index] + noten[index + 1 :]


def nach_fach(noten):
    fach_von = attrgetter("fach")
    return {
        fach: list(gruppe)
        for fach, gruppe in groupby(sorted(noten, key=fach_von), key=fach_von)
    }


def fach_schnitt(fach, noten):
    schnitt = gewichteter_durchschnitt(noten)
    return None if schnitt is None else FachSchnitt(fach, schnitt, len(noten))


def ranking_schluessel(eintrag):
    return (-eintrag.schnitt, eintrag.fach)


def faecher_ranking(noten):
    gruppen = nach_fach(noten)
    schnitte = map(fach_schnitt, gruppen.keys(), gruppen.values())
    return sorted(filter(None, schnitte), key=ranking_schluessel)


def noten_von_fach(noten: list[Note], fach: str) -> list[Note]:
    return [eintrag for eintrag in noten if eintrag.fach == fach]


def gewichtete_punkte(noten: list[Note]) -> float:
    return sum(eintrag.note * eintrag.gewicht for eintrag in noten)


def summe_gewichte(noten: list[Note]) -> float:
    return sum(eintrag.gewicht for eintrag in noten)


def benoetigte_note(punkte: float, gewichte: float, neues_gewicht: float, ziel: float) -> float:
    return (ziel * (gewichte + neues_gewicht) - punkte) / neues_gewicht


def ziel_status(note: float) -> str:
    if note < NOTE_MIN:
        return "sicher"
    if note > NOTE_MAX:
        return "unmoeglich"
    return "moeglich"


def ziel_berechnen(
    noten: list[Note], fach: str, neues_gewicht: float, ziel: float = 4.0
) -> Zielergebnis | None:
    if not 0 < neues_gewicht < math.inf:
        return None
    fach_noten = noten_von_fach(noten, fach)
    note = benoetigte_note(
        gewichtete_punkte(fach_noten), summe_gewichte(fach_noten), neues_gewicht, ziel
    )
    return Zielergebnis(fach, note, ziel_status(note))


def semester_liste(noten):
    return sorted(set(map(lambda eintrag: eintrag.semester, noten)))


def ungenuegende_noten(noten):
    return list(filter(lambda eintrag: eintrag.note < NOTE_GENUEGEND, noten))


def abstand_zu_genuegend(noten):
    return reduce(
        lambda summe, abstand: summe + abstand,
        map(lambda eintrag: NOTE_GENUEGEND - eintrag.note, ungenuegende_noten(noten)),
        0.0,
    )


def semester_statistik(noten, semester):
    im_semester = list(filter(lambda eintrag: eintrag.semester == semester, noten))
    return SemesterStatistik(
        semester=semester,
        schnitt=gewichteter_durchschnitt(im_semester),
        anzahl=len(im_semester),
        ungenuegend=len(ungenuegende_noten(im_semester)),
        abstand=abstand_zu_genuegend(im_semester),
        beste_note=max(map(lambda eintrag: eintrag.note, im_semester), default=None),
    )


def semester_statistiken(noten):
    return list(map(lambda semester: semester_statistik(noten, semester), semester_liste(noten)))


SORTIERUNGEN = {
    "erfasst": lambda zeile: zeile.index,
    "datum": lambda zeile: zeile.eintrag.datum,
    "note": lambda zeile: -zeile.eintrag.note,
    "fach": lambda zeile: zeile.eintrag.fach,
}


def noten_zeilen(noten):
    return list(map(NotenZeile, range(len(noten)), noten))


def zeilen_von_fach(zeilen, fach):
    if not fach:
        return zeilen

    def ist_im_fach(zeile):
        return zeile.eintrag.fach == fach

    return list(filter(ist_im_fach, zeilen))


def sortieren(zeilen, sortierung):
    schluessel = SORTIERUNGEN.get(sortierung, SORTIERUNGEN["erfasst"])
    return sorted(zeilen, key=schluessel)


def gesamtgewicht(zeilen):
    return reduce(lambda summe, zeile: summe + zeile.eintrag.gewicht, zeilen, 0.0)


def zahl_oder_none(text, umwandeln):
    try:
        return umwandeln(text)
    except (TypeError, ValueError):
        return None


def gueltiges_datum(text):
    try:
        date.fromisoformat(text)
    except (TypeError, ValueError):
        return False
    return True


def note_aus_formular(formular):
    fach = formular.get("fach", "").strip()
    pruefung = formular.get("pruefung", "").strip()
    note = zahl_oder_none(formular.get("note"), float)
    gewicht = zahl_oder_none(formular.get("gewicht"), float)
    semester = zahl_oder_none(formular.get("semester"), int)
    datum = formular.get("datum", "")
    pruefungen = (
        (not fach, "Das Fach fehlt."),
        (not pruefung, "Die Prüfung fehlt."),
        (note is None or not NOTE_MIN <= note <= NOTE_MAX, "Die Note muss zwischen 1 und 6 liegen."),
        (gewicht is None or not 0 < gewicht < math.inf, "Das Gewicht muss grösser als 0 sein."),
        (semester is None or semester < 1, "Das Semester muss eine ganze Zahl ab 1 sein."),
        (not gueltiges_datum(datum), "Das Datum ist ungültig."),
    )
    fehler = [meldung for ungueltig, meldung in pruefungen if ungueltig]
    if fehler:
        return None, fehler
    return Note(fach, pruefung, note, gewicht, semester, datum), []
