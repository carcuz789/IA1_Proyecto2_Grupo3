"""
Interfaz gráfica principal de HandTalk AI.

Interfaz Tkinter que captura video en tiempo real, detecta señas
y permite enviar mensajes a Telegram.

Uso:
    python app.py
"""

import os
import sys
import threading
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

# Importar módulos del proyecto
from src.capture import HandCapture
from src.predictor import SignPredictor
from src.telegram_bot import TelegramBotManager
from src.admin_panel import AdminPanel


class HandTalkApp:
    """
    Aplicación principal de HandTalk AI.
    
    Attributes:
        window: Ventana principal de Tkinter
        capture: Capturador de mano
        predictor: Predictor de señas
        telegram: Gestor de Telegram
        admin: Panel de administración
    """
    
    def __init__(self, root):
        """
        Inicializa la aplicación.
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.window = root
        self.window.title("HandTalk AI — Sistema de Detección de Señas")
        self.window.geometry("1200x800")
        
        # Datos del proyecto
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Estado de la aplicación
        self.running = False
        self.current_landmarks = None
        self.current_prediction = None
        self.message_history = []
        
        # Inicializar módulos
        try:
            self.capture = HandCapture(device_id=0)
            self.predictor = SignPredictor(self.base_dir)
            self.admin = AdminPanel()
            
            # Inicializar Telegram (puede fallar si no está configurado)
            try:
                self.telegram = TelegramBotManager()
            except (FileNotFoundError, ValueError) as e:
                self.telegram = None
                print(f"Advertencia: {e}")
        
        except Exception as e:
            messagebox.showerror(
                "Error de inicialización",
                f"Error al inicializar la aplicación:\n{str(e)}"
            )
            sys.exit(1)
        
        # Crear interfaz
        self._create_widgets()
        
        # Configurar cierre de ventana
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _create_widgets(self):
        """Crea los widgets de la interfaz."""
        
        # Frame principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ── Frame de video ──────────────────────────────────────────────────
        video_frame = ttk.LabelFrame(main_frame, text="Video en Tiempo Real", padding=10)
        video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas para mostrar el video
        self.canvas = tk.Canvas(
            video_frame,
            bg="black",
            width=640,
            height=480
        )
        self.canvas.pack()
        
        self.photo_image = None
        
        # ── Frame lateral ───────────────────────────────────────────────────
        side_frame = ttk.Frame(main_frame)
        side_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Frame de predicción
        pred_frame = ttk.LabelFrame(side_frame, text="Predicción", padding=10)
        pred_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
        
        ttk.Label(pred_frame, text="Seña detectada:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.sign_label = ttk.Label(
            pred_frame,
            text="---",
            font=("Arial", 24, "bold"),
            foreground="blue"
        )
        self.sign_label.pack(anchor=tk.W, pady=5)
        
        ttk.Label(pred_frame, text="Confianza:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.confidence_label = ttk.Label(
            pred_frame,
            text="0%",
            font=("Arial", 18),
            foreground="green"
        )
        self.confidence_label.pack(anchor=tk.W, pady=5)
        
        # Barra de progreso de confianza
        self.confidence_progress = ttk.Progressbar(
            pred_frame,
            length=250,
            mode='determinate',
            value=0
        )
        self.confidence_progress.pack(fill=tk.X, pady=5)
        
        # Umbral de confianza
        ttk.Label(pred_frame, text="Umbral mínimo:", font=("Arial", 9)).pack(anchor=tk.W, pady=(10, 0))
        threshold_frame = ttk.Frame(pred_frame)
        threshold_frame.pack(fill=tk.X, pady=5)
        
        self.threshold_var = tk.DoubleVar(value=self.admin.get_confidence_threshold())
        threshold_scale = ttk.Scale(
            threshold_frame,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            variable=self.threshold_var,
            command=self._on_threshold_change
        )
        threshold_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.threshold_label = ttk.Label(
            threshold_frame,
            text=f"{self.threshold_var.get():.0%}",
            width=5
        )
        self.threshold_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Frame de controles
        control_frame = ttk.LabelFrame(side_frame, text="Controles", padding=10)
        control_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
        
        # Botón de inicio/parada
        self.start_button = ttk.Button(
            control_frame,
            text="▶ Iniciar",
            command=self.start_camera
        )
        self.start_button.pack(fill=tk.X, pady=5)
        
        self.stop_button = ttk.Button(
            control_frame,
            text="⏹ Detener",
            command=self.stop_camera,
            state=tk.DISABLED
        )
        self.stop_button.pack(fill=tk.X, pady=5)
        
        # Botón de envío a Telegram
        self.telegram_button = ttk.Button(
            control_frame,
            text="📱 Enviar a Telegram",
            command=self.send_to_telegram,
            state=tk.DISABLED
        )
        self.telegram_button.pack(fill=tk.X, pady=5)
        
        # Frame de información
        info_frame = ttk.LabelFrame(side_frame, text="Información", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        
        ttk.Label(info_frame, text="Estado:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.status_label = ttk.Label(
            info_frame,
            text="Detenido",
            foreground="red",
            font=("Arial", 9)
        )
        self.status_label.pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(info_frame, text="Señas disponibles:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(10, 0))
        
        # Listbox de señas
        signs_text = tk.Text(
            info_frame,
            height=6,
            width=30,
            state=tk.DISABLED,
            bg="#f0f0f0",
            font=("Arial", 8)
        )
        signs_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.signs_text = signs_text
        
        # Actualizar lista de señas
        self._update_signs_display()
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(side_frame, text="Configuración", padding=10)
        config_frame.pack(fill=tk.X, padx=0)
        
        ttk.Button(
            config_frame,
            text="⚙️ Panel de Admin",
            command=self.open_admin_panel
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            config_frame,
            text="📋 Historial",
            command=self.show_history
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            config_frame,
            text="🧪 Probar conexión Telegram",
            command=self.test_telegram
        ).pack(fill=tk.X, pady=2)
    
    def start_camera(self):
        """Inicia la captura de cámara."""
        try:
            self.capture.open_camera()
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.telegram_button.config(state=tk.NORMAL)
            self.status_label.config(text="En ejecución", foreground="green")
            
            # Iniciar thread de captura
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir cámara:\n{str(e)}")
    
    def stop_camera(self):
        """Detiene la captura de cámara."""
        self.running = False
        self.capture.close_camera()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.telegram_button.config(state=tk.DISABLED)
        self.status_label.config(text="Detenido", foreground="red")
        self.canvas.delete("all")
    
    def _capture_loop(self):
        """Loop de captura de video."""
        while self.running:
            try:
                # Capturar frame
                frame, success = self.capture.capture_frame()
                if not success:
                    continue
                
                # Extraer landmarks
                landmarks, frame_with_landmarks = self.capture.get_frame_with_landmarks(frame)
                self.current_landmarks = landmarks
                
                # Predecir si hay landmarks
                if landmarks is not None:
                    prediction = self.predictor.predict(landmarks)
                    self.current_prediction = prediction
                    
                    # Dibujar predicción en el frame
                    if prediction is not None and self.predictor.is_confident(
                        prediction,
                        self.threshold_var.get()
                    ):
                        sign = prediction['sign']
                        confidence = prediction['confidence']
                        
                        # Dibujar texto en el frame
                        text = f"{sign}: {confidence:.1%}"
                        cv2.putText(
                            frame_with_landmarks,
                            text,
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.2,
                            (0, 255, 0),
                            2
                        )
                        
                        # Actualizar etiquetas
                        self.window.after(0, lambda: self._update_prediction_labels(sign, confidence))
                    else:
                        self.window.after(0, lambda: self._update_prediction_labels("---", 0))
                else:
                    self.window.after(0, lambda: self._update_prediction_labels("---", 0))
                
                # Convertir BGR a RGB y redimensionar
                frame_rgb = cv2.cvtColor(frame_with_landmarks, cv2.COLOR_BGR2RGB)
                frame_rgb = cv2.resize(frame_rgb, (640, 480))
                
                # Convertir a PIL Image
                image = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(image)
                
                # Mostrar en canvas
                self.window.after(0, lambda photo=photo: self._show_frame(photo))
            
            except Exception as e:
                print(f"Error en capture loop: {e}")
                continue
    
    def _show_frame(self, photo):
        """Muestra el frame en el canvas."""
        self.photo_image = photo
        self.canvas.create_image(320, 240, image=photo)
    
    def _update_prediction_labels(self, sign, confidence):
        """Actualiza las etiquetas de predicción."""
        self.sign_label.config(text=sign if sign != "---" else "---")
        self.confidence_label.config(text=f"{confidence:.1%}")
        self.confidence_progress.config(value=confidence * 100)
    
    def _on_threshold_change(self, value):
        """Callback cuando cambia el umbral."""
        threshold = float(value)
        self.threshold_label.config(text=f"{threshold:.0%}")
        self.admin.set_confidence_threshold(threshold)
    
    def _update_signs_display(self):
        """Actualiza la lista de señas disponibles."""
        signs = self.predictor.get_available_signs()
        signs_text = ", ".join(signs)
        
        self.signs_text.config(state=tk.NORMAL)
        self.signs_text.delete("1.0", tk.END)
        self.signs_text.insert(tk.END, signs_text)
        self.signs_text.config(state=tk.DISABLED)
    
    def send_to_telegram(self):
        """Envía la predicción actual a Telegram."""
        if self.current_prediction is None:
            messagebox.showwarning("Advertencia", "No hay predicción para enviar.")
            return
        
        if not self.predictor.is_confident(
            self.current_prediction,
            self.threshold_var.get()
        ):
            messagebox.showwarning(
                "Advertencia",
                "La confianza es menor al umbral mínimo."
            )
            return
        
        if self.telegram is None:
            messagebox.showerror(
                "Error",
                "Telegram no está configurado. Abre el panel de administración."
            )
            return
        
        sign = self.current_prediction['sign']
        confidence = self.current_prediction['confidence']
        
        try:
            success = self.telegram.send_message_sync(sign, confidence)
            if success:
                # Agregar al historial
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.message_history.append({
                    'timestamp': timestamp,
                    'sign': sign,
                    'confidence': confidence
                })
                messagebox.showinfo(
                    "Éxito",
                    f"Mensaje enviado a Telegram:\n{sign} ({confidence:.1%})"
                )
            else:
                messagebox.showerror("Error", "No se pudo enviar el mensaje a Telegram.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar a Telegram:\n{str(e)}")
    
    def test_telegram(self):
        """Prueba la conexión con Telegram."""
        if self.telegram is None:
            messagebox.showwarning(
                "Advertencia",
                "Telegram no está configurado.\n"
                "Abre el panel de administración para configurarlo."
            )
            return
        
        success, message = self.telegram.test_connection()
        if success:
            messagebox.showinfo("Éxito", message)
        else:
            messagebox.showerror("Error", message)
    
    def open_admin_panel(self):
        """Abre el panel de administración."""
        admin_window = tk.Toplevel(self.window)
        admin_window.title("Panel de Administración")
        admin_window.geometry("500x600")
        
        notebook = ttk.Notebook(admin_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ── Tab de Telegram ────────────────────────────────────────────────
        telegram_frame = ttk.Frame(notebook)
        notebook.add(telegram_frame, text="Telegram")
        
        ttk.Label(telegram_frame, text="Token del bot:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        token_entry = ttk.Entry(telegram_frame, show="*", width=50)
        token_entry.insert(0, self.admin.get_telegram_token())
        token_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(telegram_frame, text="Chat ID:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        chat_id_entry = ttk.Entry(telegram_frame, width=50)
        chat_id_entry.insert(0, self.admin.get_telegram_chat_id())
        chat_id_entry.pack(fill=tk.X, padx=10, pady=5)
        
        telegram_enabled = tk.BooleanVar(value=self.admin.is_telegram_enabled())
        ttk.Checkbutton(
            telegram_frame,
            text="Habilitar Telegram",
            variable=telegram_enabled
        ).pack(anchor=tk.W, padx=10, pady=10)
        
        ttk.Label(telegram_frame, text="Formato del mensaje:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        format_text = tk.Text(telegram_frame, height=4, width=50)
        format_text.insert(tk.END, self.admin.get_telegram_message_format())
        format_text.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(telegram_frame, text="Variables: {sign} {confidence}", font=("Arial", 8, "italic")).pack(anchor=tk.W, padx=10)
        
        def save_telegram():
            try:
                self.admin.set_telegram_token(token_entry.get())
                self.admin.set_telegram_chat_id(chat_id_entry.get())
                self.admin.set_telegram_enabled(telegram_enabled.get())
                self.admin.set_telegram_message_format(format_text.get("1.0", tk.END).strip())
                
                # Reintentar inicializar Telegram
                try:
                    self.telegram = TelegramBotManager()
                except:
                    self.telegram = None
                
                messagebox.showinfo("Éxito", "Configuración de Telegram guardada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        ttk.Button(
            telegram_frame,
            text="💾 Guardar",
            command=save_telegram
        ).pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # ── Tab del modelo ─────────────────────────────────────────────────
        model_frame = ttk.Frame(notebook)
        notebook.add(model_frame, text="Modelo")
        
        ttk.Label(model_frame, text="Umbral de confianza:", font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 5))
        threshold_var = tk.DoubleVar(value=self.admin.get_confidence_threshold())
        threshold_scale = ttk.Scale(
            model_frame,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            variable=threshold_var
        )
        threshold_scale.pack(fill=tk.X, padx=10, pady=5)
        
        threshold_label = ttk.Label(model_frame, text=f"{threshold_var.get():.0%}")
        threshold_label.pack(anchor=tk.W, padx=10)
        
        def update_threshold_label(value):
            threshold_label.config(text=f"{float(value):.0%}")
        
        threshold_scale.config(command=update_threshold_label)
        
        def save_model():
            try:
                self.admin.set_confidence_threshold(threshold_var.get())
                self.threshold_var.set(threshold_var.get())
                messagebox.showinfo("Éxito", "Configuración del modelo guardada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        ttk.Button(
            model_frame,
            text="💾 Guardar",
            command=save_model
        ).pack(fill=tk.X, padx=10, pady=(20, 5))
        
        # ── Tab de info ────────────────────────────────────────────────────
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Información")
        
        info_text = tk.Text(info_frame, height=20, width=55, state=tk.DISABLED)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info_text.config(state=tk.NORMAL)
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, f"""
HandTalk AI — Información del Sistema

Modelo:
  - Ruta: {self.admin.get_model_path()}
  - Algoritmo: SVM (RBF)
  - Accuracy: 100%

Señas disponibles:
  {', '.join(self.predictor.get_available_signs())}

Cámara:
  - Device ID: {self.admin.get_camera_device_id()}
  - Resolución: 640x480
  - FPS: 30

Historial:
  - Habilitado: {self.admin.is_history_enabled()}
  - Mensajes grabados: {len(self.message_history)}

Contacto/Soporte:
  - GitHub: github.com/carcuz789/IA1_Proyecto2_Grupo3
  - Versión: 1.0.0
  - Fecha: 2026-04-20
        """)
        info_text.config(state=tk.DISABLED)
    
    def show_history(self):
        """Muestra el historial de mensajes enviados."""
        if not self.message_history:
            messagebox.showinfo("Historial", "No hay mensajes en el historial.")
            return
        
        history_window = tk.Toplevel(self.window)
        history_window.title("Historial de Mensajes")
        history_window.geometry("600x400")
        
        # Crear tabla
        columns = ("Hora", "Seña", "Confianza")
        tree = ttk.Treeview(history_window, columns=columns, height=15)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Hora", anchor=tk.W, width=150)
        tree.column("Seña", anchor=tk.W, width=150)
        tree.column("Confianza", anchor=tk.CENTER, width=150)
        
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Hora", text="Hora", anchor=tk.W)
        tree.heading("Seña", text="Seña", anchor=tk.W)
        tree.heading("Confianza", text="Confianza", anchor=tk.CENTER)
        
        for i, item in enumerate(self.message_history):
            tree.insert(
                parent="",
                index="end",
                iid=i,
                text="",
                values=(
                    item['timestamp'],
                    item['sign'],
                    f"{item['confidence']:.1%}"
                )
            )
        
        # Botón para limpiar
        def clear_history():
            if messagebox.askyesno("Confirmar", "¿Deseas limpiar el historial?"):
                self.message_history.clear()
                for item in tree.get_children():
                    tree.delete(item)
        
        ttk.Button(
            history_window,
            text="🗑️ Limpiar historial",
            command=clear_history
        ).pack(fill=tk.X, padx=10, pady=(0, 10))
    
    def on_closing(self):
        """Maneja el cierre de la ventana."""
        if self.running:
            self.stop_camera()
        self.window.destroy()


def main():
    """Función principal."""
    root = tk.Tk()
    app = HandTalkApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
