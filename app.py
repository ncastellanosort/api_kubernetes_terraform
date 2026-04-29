from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Motor de Inferencia - Adenocarcinoma Gástrico")

CARDINALES = {
    "B1": {
        (True, False, False): 25,
        (False, True, False): 95,
        (False, False, True): 11,
        (True, True, False): 219,
        (True, False, True): 25,
        (False, True, True): 95,
        (True, True, True): 219,
        (False, False, False): 0
    },
    "B2": {
        (True, False, False): 13,
        (False, True, False): 76,
        (False, False, True): 49,
        (True, True, False): 8,
        (True, False, True): 5,
        (False, True, True): 32,
        (True, True, True): 4,
        (False, False, False): 113
    }
}

TOTAL_B1 = sum(CARDINALES["B1"].values())
TOTAL_B2 = sum(CARDINALES["B2"].values())

PRIOR_B1 = 0.7
PRIOR_B2 = 0.3

class Sintomas(BaseModel):
    dolor: bool
    perdida_peso: bool
    vomitos: bool

@app.post("/inferir")
def inferir(sintomas: Sintomas):
    evidencia = (sintomas.dolor, sintomas.perdida_peso, sintomas.vomitos)

    p_E_B1 = CARDINALES["B1"][evidencia] / TOTAL_B1
    p_E_B2 = CARDINALES["B2"][evidencia] / TOTAL_B2

    bayes_B1 = p_E_B1 * PRIOR_B1
    bayes_B2 = p_E_B2 * PRIOR_B2

    total = bayes_B1 + bayes_B2

    if total == 0:
        return {"error": "Sin datos"}

    prob_B1 = bayes_B1 / total
    prob_B2 = bayes_B2 / total

    return {
        "probabilidad_adenocarcinoma": round(prob_B1, 4),
        "probabilidad_sano": round(prob_B2, 4),
        "alerta": "CRÍTICA" if prob_B1 > 0.5 else "Normal"
    }