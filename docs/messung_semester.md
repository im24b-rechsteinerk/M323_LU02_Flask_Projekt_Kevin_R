# Messung: `semester_statistiken`

Gemessen am 08.11.2026 mit `python messung_semester.py`. Gemessen wird die Funktion direkt mit künstlichen Daten (12 Fächer, 8 Semester). Pro Grösse zählt die beste Zeit von 5 Läufen. Das Skript lief zweimal. Vor jeder Messung prüft das Skript mit `assert`, dass vorher und nachher dieselben Statistiken herauskommen.

## Teure Stelle

Vorher wurde für jedes Semester die ganze Notenliste durchsucht:

```python
def semester_statistiken(noten):
    return list(map(lambda semester: semester_statistik(noten, semester), semester_liste(noten)))
```

`semester_statistik` filtert dabei jedes Mal alle Noten. Das ist eine versteckte verschachtelte Schleife: O(Semester × Noten). cProfile mit 100'000 Noten zeigt 800'000 Aufrufe der Filter-Lambda (8 Semester × 100'000 Noten), rund die Hälfte der Laufzeit.

## Massnahme

Die Noten werden einmal nach Semester gruppiert (`nach_semester`, ein Dictionary Semester → Liste der Noten), danach wird pro Gruppe gerechnet. Das ist dieselbe Technik wie bei `nach_fach` für das Ranking. Beide nutzen jetzt `nach_attribut`.

```python
def semester_statistiken(noten):
    return [statistik_aus_gruppe(semester, gruppe) for semester, gruppe in nach_semester(noten).items()]
```

## Messwerte

| Noten | Semester | vorher Lauf 1 | nachher Lauf 1 | vorher Lauf 2 | nachher Lauf 2 | Faktor |
|---|---|---|---|---|---|---|
| 100 | 8 | 0.09 ms | 0.06 ms | 0.09 ms | 0.06 ms | 1.6 |
| 1000 | 8 | 0.66 ms | 0.52 ms | 0.66 ms | 0.35 ms | 1.3 bis 1.9 |
| 10000 | 8 | 6.63 ms | 3.53 ms | 6.50 ms | 3.33 ms | 1.9 |
| 100000 | 8 | 82.87 ms | 43.26 ms | 79.44 ms | 47.63 ms | 1.7 bis 1.9 |

Die ganze Route `/semester` braucht mit 10'000 Noten nachher rund 4 ms, inklusive Template.

## Einordnung

Die Massnahme halbiert die Laufzeit etwa, mehr nicht. Der Grund: Ein Student hat höchstens etwa 8 Semester. Die verschachtelte Schleife läuft also nur 8-mal über die Liste. Der Sprung von O(Semester × Noten) auf O(Noten log Noten) bringt deshalb einen kleinen konstanten Faktor und keinen Faktor 100 wie beim Ranking mit 500 Fächern. Den Rest der Zeit braucht die eigentliche Statistik: Summen, `reduce` und `ungenuegende_noten`. Letztere wird pro Semester zweimal berechnet und ist laut cProfile der nächste Kandidat.

Bei den echten 13 Noten in `data/noten.csv` ist der Unterschied nicht messbar. Die Änderung lohnt sich trotzdem, weil sie den Code nicht verschlechtert: Das Gruppieren nutzt dieselbe Funktion wie das Ranking, und `semester_statistiken` ist danach kürzer.

## Wahl der Datenstruktur und Preis

Gewählt ist ein Dictionary Semester → Liste der Noten. Es liefert die Noten eines Semesters direkt über den Schlüssel, statt jedes Mal alle Noten zu durchsuchen. `sorted` mit `groupby` braucht keine Mutation und liefert die Semester automatisch aufsteigend, also in derselben Reihenfolge wie vorher.

Preis:

- Zusätzlicher Speicher für die Gruppenlisten. Es sind nur Referenzen, aber pro Note eine.
- Die Sortierung kostet O(n log n). Bei sehr wenigen Semestern und sehr vielen Noten wäre ein einfacher Durchlauf, der Listen in einem Dictionary füllt, etwas schneller, bräuchte aber Mutation.
- `semester_statistik(noten, semester)` filtert für Einzelabfragen weiterhin selbst. Wer viele einzelne Semester abfragt, sollte stattdessen `nach_semester` verwenden.
