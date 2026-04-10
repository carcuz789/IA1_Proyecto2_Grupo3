"""
Script de recolección de datos para HandTalk AI.

Captura landmarks de la mano con MediaPipe y los guarda en CSV.
Usa Tkinter para el display (compatible con Wayland y X11).

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
import tkinter as tk
from PIL import Image, ImageTk

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

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    print("Iniciando cámara, espera un momento...")
    for _ in range(60):
        cap.read()

    # ── Tkinter window ────────────────────────────────────────────────────────
    root = tk.Tk()
    root.title("HandTalk AI — Recoleccion de datos")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=640, height=480, bg="black", highlightthickness=0)
    canvas.pack()

    # Panel de info debajo del canvas
    info_frame = tk.Frame(root, bg="#1e1e1e")
    info_frame.pack(fill=tk.X)

    lbl_sign   = tk.Label(info_frame, text="", font=("Courier", 14, "bold"),
                          fg="#00ff00", bg="#1e1e1e", anchor="w", padx=8)
    lbl_sign.pack(fill=tk.X)

    lbl_counts = tk.Label(info_frame, text="", font=("Courier", 11),
                          fg="#ffff00", bg="#1e1e1e", anchor="w", padx=8)
    lbl_counts.pack(fill=tk.X)

    lbl_status = tk.Label(info_frame, text="", font=("Courier", 10),
                          fg="#00d4ff", bg="#1e1e1e", anchor="w", padx=8)
    lbl_status.pack(fill=tk.X)

    lbl_keys   = tk.Label(info_frame,
                          text="[ESPACIO] Capturar   [A] Anterior   [D] Siguiente   [Q] Salir",
                          font=("Courier", 9), fg="#888888", bg="#1e1e1e", padx=8, pady=4)
    lbl_keys.pack(fill=tk.X)

    # Estado mutable compartido con los callbacks de teclado
    state = {
        "current_idx": 0,
        "session_total": 0,
        "status_msg": "Listo — coloca tu mano frente a la camara",
        "running": True,
    }

    def on_key(event):
        ch = event.keysym.lower()
        if ch == "q":
            state["running"] = False
            root.quit()
        elif ch == "d":
            state["current_idx"] = (state["current_idx"] + 1) % len(SIGNS)
            state["status_msg"] = f"-> Sena: {SIGNS[state['current_idx']]}"
        elif ch == "a":
            state["current_idx"] = (state["current_idx"] - 1) % len(SIGNS)
            state["status_msg"] = f"<- Sena: {SIGNS[state['current_idx']]}"
        elif ch == "space":
            # La captura se maneja en el loop de video
            state["capture_now"] = True

    state["capture_now"] = False
    root.bind("<KeyPress>", on_key)
    root.focus_set()

    # ── MediaPipe ─────────────────────────────────────────────────────────────
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    ) as hands:

        def update_frame():
            if not state["running"]:
                return

            ret, frame = cap.read()
            if not ret:
                root.after(30, update_frame)
                return

            frame = cv2.flip(frame, 1)
            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            current_sign  = SIGNS[state["current_idx"]]
            hand_detected = False
            features      = None

            if results.multi_hand_landmarks:
                for hand_lm in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_lm, mp_hands.HAND_CONNECTIONS
                    )
                    features      = extract_landmarks(hand_lm)
                    hand_detected = True

            # Capturar si se presionó ESPACIO
            if state["capture_now"]:
                state["capture_now"] = False
                if hand_detected and features:
                    writer.writerow(features + [current_sign])
                    counts[current_sign] += 1
                    state["session_total"] += 1
                    state["status_msg"] = (
                        f"✓ Muestra #{counts[current_sign]} guardada para '{current_sign}'"
                    )
                else:
                    state["status_msg"] = "✗ No se detecto mano — intenta de nuevo"

            # Indicador de mano en el frame
            det_color_bgr = (0, 230, 0) if hand_detected else (0, 0, 220)
            det_text      = "Mano OK" if hand_detected else "Sin mano"
            cv2.putText(frame, det_text, (frame.shape[1] - 150, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, det_color_bgr, 2)

            # Convertir a Tkinter
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            canvas.imgtk = imgtk  # evitar garbage collection
            canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

            # Actualizar labels
            lbl_sign.config(
                text=f"Sena [{state['current_idx']+1}/{len(SIGNS)}]: {current_sign}"
            )
            lbl_counts.config(
                text=f"Muestras '{current_sign}': {counts[current_sign]}  |  "
                     f"Total sesion: {state['session_total']}"
            )
            lbl_status.config(text=state["status_msg"])

            root.after(30, update_frame)  # ~33 fps

        update_frame()
        root.mainloop()

    cap.release()
    csv_file.close()

    print(f"\n{'='*50}")
    print(f"Sesion finalizada. Muestras capturadas: {state['session_total']}")
    print(f"Dataset guardado en: {OUTPUT_CSV}")
    print(f"\nResumen total por clase:")
    for sign in SIGNS:
        bar = "█" * min(counts[sign], 50)
        print(f"  {sign:12s}: {counts[sign]:4d}  {bar}")
    print("="*50)


if __name__ == "__main__":
    main()
