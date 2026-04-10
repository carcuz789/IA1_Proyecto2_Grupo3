"""
Script de entrenamiento del modelo HandTalk AI.

Carga el dataset CSV, prueba múltiples algoritmos, evalúa con métricas
y guarda el mejor modelo como model.pkl.

Uso:
    python model/train.py
"""

import json
import os
import sys

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC

# ── Rutas ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DATASET_PATH = os.path.join(BASE_DIR, "data", "processed", "dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "model", "label_encoder.pkl")
RESULTS_DIR = os.path.join(BASE_DIR, "model", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ── Candidatos de algoritmos ───────────────────────────────────────────────────
CANDIDATES = {
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "SVM": SVC(kernel="rbf", C=10, gamma="scale", probability=True),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
}


def load_data():
    if not os.path.isfile(DATASET_PATH):
        print(f"ERROR: No se encontró el dataset en {DATASET_PATH}")
        print("Ejecuta primero: python data/collect_data.py")
        sys.exit(1)

    df = pd.read_csv(DATASET_PATH)
    print(f"\nDataset cargado: {len(df)} muestras")
    print(f"Distribución por clase:\n{df['label'].value_counts().to_string()}\n")

    if df["label"].nunique() < 2:
        print("ERROR: Se necesitan al menos 2 clases para entrenar.")
        sys.exit(1)

    X = df.drop(columns=["label"]).values
    y = df["label"].values
    return X, y


def train_and_evaluate(X_train, X_test, y_train, y_test, label_names):
    results = {}

    print("=" * 60)
    print("Evaluando algoritmos...")
    print("=" * 60)

    for name, model in CANDIDATES.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
        results[name] = {
            "model": model,
            "accuracy": acc,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std(),
            "y_pred": y_pred,
        }
        print(f"\n{name}")
        print(f"  Test Accuracy : {acc:.4f}")
        print(f"  CV (5-fold)   : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    return results


def save_confusion_matrix(y_test, y_pred, labels, algo_name):
    label_indices = list(range(len(labels)))
    cm = confusion_matrix(y_test, y_pred, labels=label_indices)
    fig, ax = plt.subplots(figsize=(10, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, colorbar=True, xticks_rotation=45)
    ax.set_title(f"Matriz de Confusión — {algo_name}")
    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, f"confusion_{algo_name.replace(' ', '_')}.png")
    plt.savefig(path)
    plt.close()
    print(f"  Matriz guardada: {path}")


def main():
    print("\n🤖 HandTalk AI — Entrenamiento del modelo")

    X, y_raw = load_data()

    # Codificar etiquetas
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    label_names = le.classes_

    # Escalar features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    results = train_and_evaluate(X_train, X_test, y_train, y_test, label_names)

    # Seleccionar mejor modelo por accuracy en test
    best_name = max(results, key=lambda k: results[k]["accuracy"])
    best = results[best_name]

    print("\n" + "=" * 60)
    print(f"🏆 Mejor modelo: {best_name}  (accuracy={best['accuracy']:.4f})")
    print("=" * 60)

    # Reporte completo del mejor
    print(f"\nReporte de clasificación — {best_name}:")
    print(classification_report(y_test, best["y_pred"], target_names=label_names))

    # Guardar matrices de confusión de todos los modelos
    for name, res in results.items():
        save_confusion_matrix(y_test, res["y_pred"], label_names, name)

    # Gráfica comparativa de accuracy
    names = list(results.keys())
    accs = [results[n]["accuracy"] for n in names]
    cv_means = [results[n]["cv_mean"] for n in names]
    cv_stds = [results[n]["cv_std"] for n in names]

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(names))
    bars = ax.bar(x, accs, width=0.35, label="Test Accuracy", color="steelblue")
    ax.errorbar(x, cv_means, yerr=cv_stds, fmt="o", color="orange",
                label="CV 5-fold (media ± std)", capsize=5)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Accuracy")
    ax.set_title("Comparación de Algoritmos — HandTalk AI")
    ax.legend()
    plt.tight_layout()
    compare_path = os.path.join(RESULTS_DIR, "comparacion_algoritmos.png")
    plt.savefig(compare_path)
    plt.close()
    print(f"\nGráfica comparativa guardada: {compare_path}")

    # ── Guardar modelo, scaler y encoder ──────────────────────────────────────
    joblib.dump(best["model"], MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(le, ENCODER_PATH)

    print(f"\n✅ Modelo guardado : {MODEL_PATH}")
    print(f"✅ Scaler guardado : {SCALER_PATH}")
    print(f"✅ LabelEncoder    : {ENCODER_PATH}")

    # Actualizar config.json con las señas del encoder
    with open(CONFIG_PATH, "r") as f:
        cfg = json.load(f)
    cfg["signs"] = list(label_names)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"✅ config.json actualizado con las clases: {list(label_names)}")


if __name__ == "__main__":
    main()
