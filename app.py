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
    noten = load_noten()

    faecher_liste = []
    for eintrag in noten:
        if eintrag.fach not in faecher_liste:
            faecher_liste.append(eintrag.fach)

    zeilen = []
    for fach in faecher_liste:
        summe = 0
        gewicht_summe = 0
        anzahl = 0
        for eintrag in noten:
            if eintrag.fach == fach:
                summe += eintrag.note * eintrag.gewicht
                gewicht_summe += eintrag.gewicht
                anzahl += 1
        if gewicht_summe != 0:
            zeilen.append({"fach": fach, "schnitt": summe / gewicht_summe, "anzahl": anzahl})

    for i in range(len(zeilen)):
        for j in range(len(zeilen) - 1 - i):
            links = zeilen[j]
            rechts = zeilen[j + 1]
            if links["schnitt"] < rechts["schnitt"] or (
                links["schnitt"] == rechts["schnitt"] and links["fach"] > rechts["fach"]
            ):
                zeilen[j] = rechts
                zeilen[j + 1] = links

    return render_template("ranking.html", zeilen=zeilen)


@app.route("/ziel")
def ziel():
    return render_template(
        "platzhalter.html",
        titel="Note für 4.0",
        hinweis="Kommt später (C1).",
    )



if __name__ == "__main__":
    app.run(debug=True)
