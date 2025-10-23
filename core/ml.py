from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression

from core.models import Nota

# Mínimo de registros con nota_final para entrenar
MIN_SAMPLES = 3


def _df_seccion(seccion):
    """
    Devuelve un DataFrame con las notas de la sección indicada.
    Columnas: avance1, avance2, avance3, participacion, proyecto_final, nota_final, estudiante_id
    """
    qs = Nota.objects.filter(seccion=seccion).values(
        'avance1', 'avance2', 'avance3', 'participacion', 'proyecto_final', 'nota_final', 'estudiante_id'
    )
    df = pd.DataFrame(list(qs))
    return df


def predict_final_for_seccion(seccion):
    """
    Entrena una regresión lineal para proyectar la nota final.
    Requiere al menos MIN_SAMPLES registros con nota_final en la sección.
    Retorna: dict con métricas y predicciones por estudiante.
    """
    df = _df_seccion(seccion)

    # registros con etiqueta (nota_final) para entrenar
    train = df.dropna(subset=['nota_final']).copy()
    if len(train) < MIN_SAMPLES:
        raise ValueError(f"Se requieren al menos {MIN_SAMPLES} registros con nota final para entrenar.")

    X = train[['avance1', 'avance2', 'avance3', 'participacion', 'proyecto_final']].fillna(0.0).to_numpy(dtype=float)
    y = train['nota_final'].to_numpy(dtype=float)

    model = LinearRegression()
    model.fit(X, y)
    r2 = float(model.score(X, y))

    # Predecimos para todos los alumnos de la sección
    X_all = df[['avance1', 'avance2', 'avance3', 'participacion', 'proyecto_final']].fillna(0.0).to_numpy(dtype=float)
    preds = model.predict(X_all)

    out = []
    for i, row in df.iterrows():
        out.append({
            "estudiante": int(row['estudiante_id']),
            "pred_final": float(np.clip(preds[i], 0, 20))  # acotamos 0..20 por estética
        })

    return {"metrics": {"type": "linear_regression", "r2": r2, "n_train": int(len(train))},
            "predictions": out}


def predict_risk_for_seccion(seccion, umbral_aprueba: float = 11.0):
    """
    Entrena una regresión logística para estimar probabilidad de riesgo (reprueba).
    Requiere al menos MIN_SAMPLES y que existan dos clases en el conjunto de entrenamiento.
    Retorna: dict con métricas y predicciones por estudiante (probabilidad de riesgo).
    """
    df = _df_seccion(seccion)

    train = df.dropna(subset=['nota_final']).copy()
    if len(train) < MIN_SAMPLES:
        raise ValueError(f"Se requieren al menos {MIN_SAMPLES} registros con nota final para entrenar.")

    X = train[['avance1', 'avance2', 'avance3', 'participacion', 'proyecto_final']].fillna(0.0).to_numpy(dtype=float)
    y = (train['nota_final'].to_numpy(dtype=float) < umbral_aprueba).astype(int)  # 1 = riesgo

    # Evitar fallo si todas las clases son iguales
    if len(np.unique(y)) < 2:
        raise ValueError("No hay diversidad de clases para entrenar el modelo de riesgo.")

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, y)
    acc = float(clf.score(X, y))

    X_all = df[['avance1', 'avance2', 'avance3', 'participacion', 'proyecto_final']].fillna(0.0).to_numpy(dtype=float)
    probas = clf.predict_proba(X_all)[:, 1]  # probabilidad de riesgo

    out = []
    for i, row in df.iterrows():
        out.append({
            "estudiante": int(row['estudiante_id']),
            "risk_prob": float(probas[i])  # 0..1
        })

    return {"metrics": {"type": "logistic_regression", "accuracy": acc, "n_train": int(len(train))},
            "predictions": out}
