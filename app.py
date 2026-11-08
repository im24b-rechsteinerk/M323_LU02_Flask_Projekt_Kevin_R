from http import HTTPStatus

from flask import Flask, flash, redirect, render_template, request, url_for

from logic import (
    STANDARD_SORTIERUNG,
    faecher,
    faecher_ranking,
    gesamtgewicht,
    gewichteter_durchschnitt,
    hinzufuegen,
    note_aus_formular,
    note_delete,
    noten_zeilen,
    semester_statistiken,
    sortieren,
    zeilen_von_fach,
    ziel_berechnen,
)
from storage import load_noten, save_noten

app = Flask(__name__)
app.secret_key = "notenrechner-dev"


@app.route("/")
def index():
    return redirect(url_for("notenliste"))


@app.route("/noten")
def notenliste():
    noten = load_noten()
    fach = request.args.get("fach", "")
    sortierung = request.args.get("sortierung", STANDARD_SORTIERUNG)
    zeilen = sortieren(zeilen_von_fach(noten_zeilen(noten), fach), sortierung)
    return render_template(
        "noten.html",
        zeilen=zeilen,
        schnitt=gewichteter_durchschnitt([zeile.eintrag for zeile in zeilen]),
        gesamtgewicht=gesamtgewicht(zeilen),
        faecher=faecher(noten),
        fach=fach,
        sortierung=sortierung,
    )


@app.route("/erfassen", methods=["GET", "POST"])
def erfassen():
    noten = load_noten()
    if request.method != "POST":
        return render_template("erfassen.html", faecher=faecher(noten), fehler=[], werte={})
    neue, fehler = note_aus_formular(request.form)
    if fehler:
        return (
            render_template("erfassen.html", faecher=faecher(noten), fehler=fehler, werte=request.form),
            HTTPStatus.BAD_REQUEST,
        )
    save_noten(hinzufuegen(noten, neue))
    flash("Note gespeichert.")
    return redirect(url_for("notenliste"))


@app.route("/loeschen/<int:index>", methods=["POST"])
def loeschen(index):
    noten = load_noten()
    if 0 <= index < len(noten):
        save_noten(note_delete(noten, index))
        flash("Note gelöscht.")
    return redirect(url_for("notenliste"))


@app.route("/semester")
def semester():
    return render_template("semester.html", zeilen=semester_statistiken(load_noten()))


@app.route("/ranking")
def ranking():
    return render_template("ranking.html", zeilen=faecher_ranking(load_noten()))


@app.route("/ziel")
def ziel():
    noten = load_noten()
    fach = request.args.get("fach", "")
    gewicht = request.args.get("gewicht", 1.0, type=float)
    return render_template(
        "ziel.html",
        faecher=faecher(noten),
        fach=fach,
        gewicht=gewicht,
        ergebnis=ziel_berechnen(noten, fach, gewicht) if fach else None,
    )



if __name__ == "__main__":
    app.run(debug=True)
