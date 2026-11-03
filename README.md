# Notenrechner

Flask-Applikation zum Erfassen und Auswerten von Prüfungsnoten. Praxisprojekt für die LB02 im Modul M323 (Funktional Programmieren).

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Starten

```bash
python app.py
```

Die App läuft danach auf http://127.0.0.1:5000.

## Tests

```bash
pytest
```

## Funktionen

| Seite | Route | Stand |
|---|---|---|
| Notenliste mit gewichtetem Durchschnitt und Löschen | `/noten` | fertig |
| Note erfassen | `/erfassen` | fertig |
| Semesterstatistik | `/semester` | fertig |
| Fächer-Ranking | `/ranking` | fertig |
| Note für 4.0 | `/ziel` | fertig |

## Aufbau

| Pfad | Inhalt |
|---|---|
| `app.py` | Flask-Routen |
| `logic.py` | Datentyp `Note` und pure Funktionen |
| `storage.py` | CSV lesen und schreiben, einzige Stelle mit I/O |
| `data/noten.csv` | Notendaten |
| `templates/`, `static/` | HTML-Templates und CSS |
| `tests/` | Tests für `logic.py`, `storage.py`, das Ranking, die Note für 4.0 und die Semesterstatistik |
| `docs/` | Design-Blätter |
