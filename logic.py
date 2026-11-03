import math
from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter

NOTE_MIN = 1.0
NOTE_MAX = 6.0


@dataclass(frozen=True)
class Note:
    fach: str
    pruefung: str
    note: float
    gewicht: float
    semester: int
    datum: str


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
