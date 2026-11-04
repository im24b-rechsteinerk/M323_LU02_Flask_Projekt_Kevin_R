"""Gewichteter Durchschnitt prozedural und objektorientiert, als Vergleich zur funktionalen Variante.

Die App nutzt nur `gewichteter_durchschnitt` aus logic.py. Dieses Modul dient dem Paradigmenvergleich.
"""


def durchschnitt_prozedural(noten):
    summe = 0.0
    gewicht_summe = 0.0
    for eintrag in noten:
        summe += eintrag.note * eintrag.gewicht
        gewicht_summe += eintrag.gewicht
    if gewicht_summe == 0:
        return None
    return summe / gewicht_summe


class Notenbuch:
    def __init__(self, noten=()):
        self._noten = list(noten)
        self._summe = 0.0
        self._gewicht_summe = 0.0
        for eintrag in self._noten:
            self._summe += eintrag.note * eintrag.gewicht
            self._gewicht_summe += eintrag.gewicht

    def hinzufuegen(self, eintrag):
        self._noten.append(eintrag)
        self._summe += eintrag.note * eintrag.gewicht
        self._gewicht_summe += eintrag.gewicht

    def durchschnitt(self):
        if self._gewicht_summe == 0:
            return None
        return self._summe / self._gewicht_summe
