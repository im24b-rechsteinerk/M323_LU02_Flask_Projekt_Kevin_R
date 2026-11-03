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

Noch nicht gemessen.
