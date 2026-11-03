from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter


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
