from flask import Flask, flash, redirect, render_template, request, url_for

from logic import Note, faecher, gewichteter_durchschnitt, hinzufuegen, note_delete
from storage import load_noten, save_noten

app = Flask(__name__)
app.secret_key = "notenrechner-dev"


@app.route("/")
def index():
    return redirect(url_for("notenliste"))


@app.route("/noten")
def notenliste():
    noten = load_noten()
    return render_template(
        "noten.html",
        noten=noten,
        schnitt=gewichteter_durchschnitt(noten),
    )


@app.route("/erfassen", methods=["GET", "POST"])
def erfassen():
    noten = load_noten()
    if request.method == "POST":
        neue = Note(
            fach=request.form["fach"].strip(),
            pruefung=request.form["pruefung"].strip(),
            note=float(request.form["note"]),
            gewicht=float(request.form["gewicht"]),
            semester=int(request.form["semester"]),
            datum=request.form["datum"],
        )
        save_noten(hinzufuegen(noten, neue))
        flash("Note gespeichert.")
        return redirect(url_for("notenliste"))
    return render_template("erfassen.html", faecher=faecher(noten))


@app.route("/loeschen/<int:index>", methods=["POST"])
def loeschen(index):
    noten = load_noten()
    if 0 <= index < len(noten):
        save_noten(note_delete(noten, index))
        flash("Note gelöscht.")
    return redirect(url_for("notenliste"))


@app.route("/semester")
def semester():
    return render_template(
        "platzhalter.html",
        titel="Semesterstatistik",
        hinweis="Kommt später (C2I).",
    )


@app.route("/ranking")
def ranking():
    return render_template(
        "platzhalter.html",
        titel="Fächer-Ranking",
        hinweis="Zuerst Design-Blatt, dann imperative Route.",
    )


@app.route("/ziel")
def ziel():
    return render_template(
        "platzhalter.html",
        titel="Note für 4.0",
        hinweis="Kommt später (C1).",
    )



if __name__ == "__main__":
    app.run(debug=True)
