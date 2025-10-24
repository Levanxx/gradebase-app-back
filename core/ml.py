from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from core.models import Nota

# Mínimo de registros con nota_final válida para entrenar
MIN_SAMPLES = 3
UMBRAL_RIESGO = 0.6  # probabilidad >= 0.6 se considera ALTO riesgo


def _df_seccion(seccion):
    """
    Devuelve un DataFrame ordenado con las notas de la sección indicada.
    Columnas: avance1, avance2, avance3, participacion, proyecto_final,
              nota_final, estudiante_id, estudiante__codigo
    """
    qs = (
        Nota.objects.filter(seccion=seccion)
        .select_related("estudiante")
        .order_by("estudiante_id")
        .values(
            "avance1",
            "avance2",
            "avance3",
            "participacion",
            "proyecto_final",
            "nota_final",
            "estudiante_id",
            "estudiante__codigo",
        )
    )
    df = pd.DataFrame(list(qs))
    return df


def predict_final_for_seccion(seccion):
    """
    Entrena una regresión lineal para proyectar la nota final.
    Requiere al menos MIN_SAMPLES registros con nota_final > 0.
    Retorna: dict con métricas y predicciones por estudiante.
    """
    df = _df_seccion(seccion)

    # registros con etiqueta válida (>0)
    train = df[df["nota_final"] > 0].copy()
    if len(train) < MIN_SAMPLES:
        raise ValueError(
            f"Se requieren al menos {MIN_SAMPLES} registros con nota_final > 0 para entrenar."
        )

    X = (
        train[["avance1", "avance2", "avance3", "participacion", "proyecto_final"]]
        .fillna(0.0)
        .to_numpy(dtype=float)
    )
    y = train["nota_final"].to_numpy(dtype=float)

    model = LinearRegression()
    model.fit(X, y)
    y_pred_train = model.predict(X)

    # Métricas
    r2 = float(model.score(X, y))
    mae = float(mean_absolute_error(y, y_pred_train))
    rmse = float(np.sqrt(mean_squared_error(y, y_pred_train)))

    # Predecimos para todos los alumnos de la sección
    X_all = (
        df[["avance1", "avance2", "avance3", "participacion", "proyecto_final"]]
        .fillna(0.0)
        .to_numpy(dtype=float)
    )
    preds = model.predict(X_all)

    out = []
    for i, row in df.iterrows():
        out.append(
            {
                "codigo": row["estudiante__codigo"],
                "estudiante": int(row["estudiante_id"]),
                "pred_final": float(np.clip(preds[i], 0, 20)),  # limitar a 0–20
            }
        )

    return {
        "metrics": {
            "type": "linear_regression",
            "r2": r2,
            "mae": mae,
            "rmse": rmse,
            "n_train": int(len(train)),
            "version": "v1",
        },
        "predictions": out,
    }


def predict_risk_for_seccion(seccion, umbral_aprueba: float = 11.0):
    """
    Entrena una regresión logística para estimar probabilidad de riesgo (reprueba).
    Requiere al menos MIN_SAMPLES y dos clases distintas.
    Retorna: dict con métricas y predicciones por estudiante.
    """
    df = _df_seccion(seccion)

    train = df[df["nota_final"] > 0].copy()
    if len(train) < MIN_SAMPLES:
        raise ValueError(
            f"Se requieren al menos {MIN_SAMPLES} registros con nota_final > 0 para entrenar."
        )

    X = (
        train[["avance1", "avance2", "avance3", "participacion", "proyecto_final"]]
        .fillna(0.0)
        .to_numpy(dtype=float)
    )
    y = (train["nota_final"].to_numpy(dtype=float) < umbral_aprueba).astype(int)  # 1 = riesgo

    # Evitar fallo si todas las clases son iguales
    if len(np.unique(y)) < 2:
        raise ValueError("No hay diversidad de clases para entrenar el modelo de riesgo.")

    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    clf.fit(X, y)
    acc = float(clf.score(X, y))

    X_all = (
        df[["avance1", "avance2", "avance3", "participacion", "proyecto_final"]]
        .fillna(0.0)
        .to_numpy(dtype=float)
    )
    probas = clf.predict_proba(X_all)[:, 1]  # probabilidad de riesgo

    out = []
    for i, row in df.iterrows():
        prob = float(probas[i])
        if prob >= UMBRAL_RIESGO:
            clase = "ALTO"
        elif prob >= 0.3:
            clase = "MEDIO"
        else:
            clase = "BAJO"
        out.append(
            {
                "codigo": row["estudiante__codigo"],
                "estudiante": int(row["estudiante_id"]),
                "risk_prob": prob,
                "clase": clase,
                "umbral": UMBRAL_RIESGO,
            }
        )

    return {
        "metrics": {
            "type": "logistic_regression",
            "accuracy": acc,
            "n_train": int(len(train)),
            "version": "v1",
        },
        "predictions": out,
    }
