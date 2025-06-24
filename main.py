from fastapi import FastAPI, Query
from pydantic import BaseModel
import csv

# Initialisation de l'API
app = FastAPI()

# Charger le vocabulaire au démarrage sous forme de liste de dicts : [{"mot": ..., "occurrence": ...}, ...]
def charger_vocabulaire(fichier_csv):
    vocab = []
    with open(fichier_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convertir occurrence en int
            row['occurrence'] = int(row['occurrence'])
            vocab.append(row)
    return vocab

# Modèle de requête
class PredictionRequest(BaseModel):
    prefix: str
    top_k: int = 3

vocabulaire = charger_vocabulaire('mots_avec_occurrence.csv')

def predict_words_by_prefix(prefix, vocab, top_k=3):
    prefix = prefix.lower()
    # Filtrer les mots qui commencent par le préfixe
    filtres = [entry for entry in vocab if entry['mot'].startswith(prefix)]
    # Trier par occurrence décroissante
    filtres.sort(key=lambda x: x['occurrence'], reverse=True)
    # Retourner les top_k suggestions avec mot + occurrence
    return filtres[:top_k]


@app.post("/predict")
def predict(request: PredictionRequest):
    result = predict_words_by_prefix(request.prefix, vocabulaire, top_k=request.top_k)


    # return result

    if result:
        return {
        "predictions": [
            {"word": entry["mot"], "occurrence": entry["occurrence"]}
            for entry in result
        ]
    }
    else:
        return {"message": "Aucune prédiction disponible pour le prefix donnée."}