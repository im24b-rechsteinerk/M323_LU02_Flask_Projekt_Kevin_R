# Design-Blatt: Fächer-Ranking

Feature: Seite `/ranking`. Sie zeigt, in welchen Fächern die Noten am besten und am schlechtesten sind.

Dieses Design entsteht vor dem Code.

## Deklarative Anforderungen

Die Anforderungen beschreiben, was gelten muss, nicht wie es berechnet wird.

1. Jedes Fach mit einem berechenbaren Durchschnitt kommt genau einmal im Ranking vor.
2. Der Fachschnitt ist der gewichtete Durchschnitt aller Noten dieses Fachs.
3. Ein Fach, dessen Gewichte zusammen 0 ergeben, kommt nicht im Ranking vor.
4. Das Ranking ist nach Fachschnitt absteigend sortiert.
5. Bei gleichem Fachschnitt sind die Fächer alphabetisch sortiert.
6. Der Rang ist die Position im sortierten Ranking, beginnend bei 1.
7. Ohne Noten ist das Ranking leer.
8. Die Eingabedaten bleiben unverändert.

## Datenfluss

```text
data/noten.csv
    | load_noten (I/O, storage.py)
    v
list[Note]
    | nach_fach
    v
dict[str, list[Note]]
    | fach_schnitt, pro Fach
    v
list[FachSchnitt | None]
    | filter: Fächer ohne Schnitt entfernen
    v
list[FachSchnitt]
    | sorted mit ranking_schluessel
    v
sortierte list[FachSchnitt]
    | render_template (Route, app.py)
    v
HTML-Tabelle: Rang, Fach, Schnitt, Anzahl Noten
```

Nur der Anfang und das Ende haben Nebeneffekte. Alles dazwischen sind pure Funktionen in `logic.py`.

## Datentyp

```python
@dataclass(frozen=True)
class FachSchnitt:
    fach: str
    schnitt: float
    anzahl: int
```

`frozen=True` macht den Typ immutable, wie bei `Note`. Der Konstruktor ist `FachSchnitt(...)`.

## Geplante Operatoren

| Operator | Signatur | Aufgabe |
|---|---|---|
| `nach_fach` | `(list[Note]) -> dict[str, list[Note]]` | Gruppiert die Noten nach Fach, mit `reduce` |
| `fach_schnitt` | `(str, list[Note]) -> FachSchnitt \| None` | Berechnet den Schnitt eines Fachs mit `gewichteter_durchschnitt`, `None` ohne berechenbaren Schnitt |
| `ranking_schluessel` | `(FachSchnitt) -> tuple[float, str]` | Liefert den Sortierschlüssel `(-schnitt, fach)` |
| `faecher_ranking` | `(list[Note]) -> list[FachSchnitt]` | Setzt die Operatoren zum ganzen Ablauf zusammen |

`gewichteter_durchschnitt` gibt es schon und wird wiederverwendet. `ranking_schluessel` ist bewusst eine benannte Funktion, weil ein Lambda mit Tupel und Minuszeichen schlechter lesbar wäre.

## Testfälle

| Fall | Input | Erwarteter Output |
|---|---|---|
| Echte Daten | `data/noten.csv` mit 13 Noten | Informatik 4.875, Englisch 4.75, Mathematik 4.30, Wirtschaft 4.00 |
| Keine Noten | `[]` | `[]` |
| Gewicht 0 | Fach A mit Note 5.0 und Gewicht 0 | `[]` |
| Gleichstand | Biologie 5.0, Chemie 5.0 in beliebiger Reihenfolge | Biologie vor Chemie |
| Gewichtung | Note 4.0 mit Gewicht 2, Note 5.5 mit Gewicht 1 | Schnitt 4.5 |
| Unveränderte Eingabe | Liste vor und nach dem Aufruf vergleichen | Liste ist gleich |

Zum ersten Fall, gerechnet als Summe aus Note mal Gewicht geteilt durch Summe der Gewichte:

| Fach | Rechnung | Schnitt | Noten |
|---|---|---|---|
| Informatik | 19.5 / 4 | 4.875 | 3 |
| Englisch | 14.25 / 3 | 4.75 | 4 |
| Mathematik | 21.5 / 5 | 4.30 | 4 |
| Wirtschaft | 8 / 2 | 4.00 | 2 |

## Umsetzung in zwei Schritten

1. Die Route `/ranking` wird zuerst imperativ gebaut: mit Schleifen direkt in der Route und einer eigenen Commit-Version.
2. Danach wird sie mit den Operatoren oben deklarativ umgesetzt. Dieselben Tests müssen in beiden Versionen bestehen.

## Abweichung bei der Umsetzung

Dieser Abschnitt kam nach dem ersten Design dazu.

`nach_fach` nutzt `sorted` und `groupby` statt `reduce`. Eine `reduce`-Variante ohne Mutation müsste bei jedem Schritt Dictionary und Liste kopieren und war bei 10000 Noten und 500 Fächern über 20-mal langsamer. Eine schnelle `reduce`-Variante müsste ein Dictionary verändern. Die Zahlen stehen in `docs/messung_ranking.md`.
