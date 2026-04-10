"""
Script de recolección de datos para HandTalk AI.

Captura landmarks de la mano con MediaPipe y los guarda en CSV.

Uso:
    python data/collect_data.py

Controles:
    A / D   : cambiar seña anterior/siguiente
    ESPACIO : capturar muestra
    Q       : guardar y salir
"""

import csv
import json
import os
import sys

import cv2
import mediapipe as mp

# ── Configuración ──────────────────────────────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

SIGNS = config["signs"]
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "dataset.csv")

# ── MediaPipe ──────────────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def build_header():
    header = []
    for i in range(21):
        header += [f"x{i}", f"y{i}", f"z{i}"]
    header.append("label")
    return header


def extract_landmarks(hand_landmarks):
    """Devuelve lista de 63 floats (x, y, z) por cada landmark."""
    landmarks = []
    for lm in hand_landmarks.landmark:
        landmarks.extend([lm.x, lm.y, lm.z])
    return landmarks


def load_counts():
    """Cuenta cuántas muestras hay por clase en el CSV existente."""
    counts = {sign: 0 for sign in SIGNS}
    if not os.path.isfile(OUTPUT_CSV):
        return counts
    with open(OUTPUT_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row.get("label", "")
            if label in counts:
                counts[label] += 1
    return counts


def main():
    file_exists = os.path.isfile(OUTPUT_CSV)
    csv_file = open(OUTPUT_CSV, "a", newline="")
    writer = csv.writer(csv_file)
    if not file_exists:
        writer.writerow(build_header())

    counts = load_counts()
    cap = cv2.VideoCapture(config["camera"]["device_id"])
    if not cap.isOpened():
        print("ERROR: No se pudo abrir la cámara.")
        sys.exit(1)

    current_idx = 0
    session_total = 0
    status_msg = "Listo — coloca tu mano frente a la cámara"

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    ) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            current_sign = SIGNS[current_idx]
            hand_detected = False
            features = None

            # Dibujar landmarks si hay mano
            if results.multi_hand_landmarks:
                for hand_lm in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_lm, mp_hands.HAND_CONNECTIONS
                    )
                    features = extract_landmarks(hand_lm)
                    hand_detected = True

            # ── Panel de información ───────────────────────────────────────────
            h, w = frame.shape[:2]
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, 115), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

            cv2.putText(frame, f"Sena: [{current_idx + 1}/{len(SIGNS)}] {current_sign}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 0), 2)
            cv2.putText(frame,
                        f"Muestras '{current_sign}': {counts[current_sign]}  |  Total sesion: {session_total}",
                        (10, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (255, 255, 0), 2)
            cv2.putText(frame, "[ESPACIO] Capturar   [A] Anterior   [D] Siguiente   [Q] Salir",
                        (10, 94), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (180, 180, 180), 1)

            det_color = (0, 230, 0) if hand_detected else (0, 0, 220)
            det_text = "Mano OK" if hand_detected else "Sin mano"
            cv2.putText(frame, det_text, (w - 150, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, det_color, 2)

            cv2.putText(frame, status_msg, (10, h - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 210, 255), 2)

            cv2.imshow("HandTalk AI — Recoleccion de datos", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            elif key == ord("d"):
                current_idx = (current_idx + 1) % len(SIGNS)
                status_msg = f"-> Sena: {SIGNS[current_idx]}"
            elif key == ord("a"):
                current_idx = (current_idx - 1) % len(SIGNS)
                status_msg = f"<- Sena: {SIGNS[current_idx]}"
            elif key == ord(" "):
                if hand_detected and features:
                    writer.writerow(features + [current_sign])
                    counts[current_sign] += 1
                    session_total += 1
                    status_msg = (
                        f"✓ Muestra #{counts[current_sign]} guardada para '{current_sign}'"
                    )
                else:
                    status_msg = "✗ No se detecto mano — intenta de nuevo"

    cap.release()
    cv2.destroyAllWindows()
    csv_file.close()

    print(f"\n{'='*50}")
    print(f"Sesion finalizada. Muestras capturadas: {session_total}")
    print(f"Dataset guardado en: {OUTPUT_CSV}")
    print(f"\nResumen total por clase:")
    for sign in SIGNS:
        bar = "█" * min(counts[sign], 50)
        print(f"  {sign:12s}: {counts[sign]:4d}  {bar}")
    print("="*50)


if __name__ == "__main__":
    main()
