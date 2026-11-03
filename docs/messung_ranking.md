# Messung: Route `/ranking`

Gemessen mit `python messung_ranking.py`. Die Route läuft über den Flask-Test-Client mit künstlichen Daten, inklusive Template. Pro Grösse zählt die beste Zeit von 5 Läufen. Das Skript lief zweimal.

## Vorher: imperative Route

Stand: geschachtelte Schleifen direkt in der Route, Sortierung mit Bubblesort.

| Noten | Fächer | Lauf 1 | Lauf 2 |
|---|---|---|---|
| 1000 | 10 | 1.0 ms | 1.1 ms |
| 10000 | 50 | 20.1 ms | 21.0 ms |
| 10000 | 500 | 213.4 ms | 200.1 ms |

Bei gleich vielen Noten und zehnmal mehr Fächern dauert die Route rund zehnmal länger, weil für jedes Fach alle Noten durchsucht werden.

## Nachher: deklarative Route

Stand: `faecher_ranking` in `logic.py`, einmal gruppieren mit `sorted` und `groupby`, ein Dictionary pro Fach, Sortierung mit `sorted`.

| Noten | Fächer | Lauf 1 | Lauf 2 |
|---|---|---|---|
| 1000 | 10 | 0.8 ms | 0.8 ms |
| 10000 | 50 | 3.7 ms | 3.4 ms |
| 10000 | 500 | 6.0 ms | 6.1 ms |

Bei 10000 Noten und 500 Fächern sinkt die Zeit von rund 200 ms auf rund 6 ms. Mit wenigen Fächern ist der Gewinn klein: Bei 1000 Noten und 10 Fächern sind es nur 0.2 bis 0.3 ms. Bei den 13 echten Noten ist der Unterschied nicht spürbar.

## Wahl der Datenstruktur

Einzelmessung von `nach_fach` allein, mit denselben künstlichen Daten. Das Vergleichsskript ist nicht Teil des Projekts.

| Variante | 1000 Noten, 10 Fächer | 10000 Noten, 50 Fächer | 10000 Noten, 500 Fächer |
|---|---|---|---|
| `reduce`, kopiert Dictionary und Liste bei jedem Schritt | 0.59 ms | 11.34 ms | 36.78 ms |
| `reduce`, verändert ein internes Dictionary | 0.12 ms | 1.16 ms | 1.21 ms |
| `sorted` und `groupby` | 0.18 ms | 1.86 ms | 1.54 ms |

Gewählt ist `sorted` und `groupby` mit einem Dictionary pro Fach. Das Dictionary liefert die Noten eines Fachs direkt über den Namen, statt für jedes Fach alle Noten zu durchsuchen. Die Variante braucht keine Mutation und ist 1.3- bis 1.6-mal langsamer als die schnellste, was hier nicht ins Gewicht fällt.
