"""
Genera datos de prueba para entrenar el modelo.
Útil cuando no hay suficientes muestras reales.
"""
import csv
import json
import os
import numpy as np
import pandas as pd

# Configurar rutas
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "processed", "dataset.csv")

# Leer configuración
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

SIGNS = config["signs"]
SAMPLES_PER_CLASS = 80  # Muestras por clase

print(f"Generando {len(SIGNS)} clases x {SAMPLES_PER_CLASS} muestras = {len(SIGNS) * SAMPLES_PER_CLASS} total")
print(f"Clases: {', '.join(SIGNS)}\n")

# Crear dataset
data = []
header = []
for i in range(21):
    header += [f"x{i}", f"y{i}", f"z{i}"]
header.append("label")

np.random.seed(42)

for sign_idx, sign in enumerate(SIGNS):
    # Generar datos con patrón único por clase
    # Variación pequeña para simular diferentes ángulos/poses
    base_x = sign_idx / len(SIGNS)
    base_y = 0.5
    base_z = 0.3
    
    for _ in range(SAMPLES_PER_CLASS):
        # 63 features (21 landmarks × 3 coordenadas)
        landmarks = []
        for i in range(21):
            # Añadir ruido gaussiano al patrón base
            x = base_x + np.random.normal(0, 0.05)
            y = base_y + np.random.normal(0, 0.05)
            z = base_z + np.random.normal(0, 0.02)
            # Mantener dentro de rango [0, 1]
            x = np.clip(x, 0, 1)
            y = np.clip(y, 0, 1)
            z = np.clip(z, 0, 1)
            landmarks.extend([x, y, z])
        
        landmarks.append(sign)
        data.append(landmarks)

# Guardar a CSV
print(f"Guardando en: {OUTPUT_CSV}\n")
df = pd.DataFrame(data, columns=header)
df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Dataset de prueba generado: {len(df)} muestras")
print(f"\nDistribución:")
print(df['label'].value_counts().sort_index())
print(f"\n📝 Nota: Estos datos son para PRUEBA solamente.")
print(f"Para mejor precisión, ejecuta: python data/collect_data.py")
