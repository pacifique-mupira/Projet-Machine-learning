from flask import Flask, render_template, request, redirect

# importation de joblib pour charger notre modele
import joblib 
import math
import pandas as pd

# creation de l'application flask
app = Flask(__name__)

# chargement du modele
modele = joblib.load("monModeleML.joblib")

# creation de l'api

@app.route("/", methods=['POST', 'GET'])
def index():
    resultat = None
    erreur = None

    # requiperation des données du formulaire
    heures = request.form.get("heures_etude", "")
    note = request.form.get("note_partiel", "")

    if request.method == 'POST':
        try:
            h,n = float(heures), float(note)
            if not (math.isfinite(h) and math.isfinite(n) and 0 <= h <= 10 and 0 <= n <= 10):
                raise ValueError()
        except ValueError:
            erreur = "Saisissez les heures et notes comprises entre 0 et 10"
            return render_template('index.html', erreur = erreur, heures = heures, note = note)

        X = pd.DataFrame([[h,n]], columns=['heures_etude', 'note_partiel'])
        prediction = int(modele.predict(X)[0]) 

        resultat = {
            0: "Vous avez la probabilité d'échouer",
            1: "Vous avez la probabilité de reussir"

        }[prediction]

    return render_template('index.html', resultat = resultat, erreur = erreur, heures = heures, note = note)

if __name__ == "__main__":
    app.run(debug=True)