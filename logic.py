from dataclasses import dataclass


@dataclass(frozen=True)
class Note:
    fach: str
    pruefung: str
    note: float
    gewicht: float
    semester: int
    datum: str


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