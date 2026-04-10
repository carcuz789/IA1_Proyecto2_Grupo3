"""
Módulo de captura de video en tiempo real y extracción de landmarks de la mano.

Utiliza OpenCV para capturar video y MediaPipe Hands para detectar
los 21 puntos de referencia (landmarks) de la mano.
"""

import cv2
import mediapipe as mp
import numpy as np


class HandCapture:
    """
    Captura video en tiempo real y extrae landmarks de la mano.
    
    Attributes:
        device_id (int): ID del dispositivo de cámara (por defecto 0)
        mp_hands: Inicializador de MediaPipe Hands
        hands: Detector de manos
        drawing_utils: Utilidades de dibujo de MediaPipe
        drawing_styles: Estilos de dibujo de MediaPipe
    """
    
    def __init__(self, device_id=0):
        """
        Inicializa el capturador de mano.
        
        Args:
            device_id (int): ID del dispositivo de cámara
        """
        self.device_id = device_id
        self.cap = None
        
        # Inicializar MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.drawing_utils = mp.solutions.drawing_utils
        self.drawing_styles = mp.solutions.drawing_styles
        
        # MP Drawing options
        self.hand_landmarks_style = self.drawing_styles.get_default_hand_landmarks_style()
        self.hand_connections_style = self.drawing_styles.get_default_hand_connections_style()
    
    def open_camera(self):
        """Abre la cámara web."""
        self.cap = cv2.VideoCapture(self.device_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la cámara en device_id={self.device_id}")
        
        # Configurar resolución y FPS
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
    
    def close_camera(self):
        """Cierra la cámara."""
        if self.cap is not None:
            self.cap.release()
    
    def capture_frame(self):
        """
        Captura un frame de la cámara.
        
        Returns:
            tuple: (frame, success) - frame capturado y booleano de éxito
        """
        if self.cap is None:
            raise RuntimeError("La cámara no está abierta. Ejecuta open_camera() primero.")
        
        success, frame = self.cap.read()
        return frame, success
    
    def extract_landmarks(self, frame):
        """
        Extrae los 21 landmarks de la mano del frame.
        
        Args:
            frame: Imagen del frame en formato BGR
            
        Returns:
            tuple: (landmarks, frame_rgb, results)
                - landmarks: array (63,) = 21 puntos × 3 coordenadas (x, y, z)
                - frame_rgb: frame convertido a RGB
                - results: objeto de resultados de MediaPipe
        """
        # Convertir BGR a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        
        # Detectar manos
        results = self.hands.process(frame_rgb)
        
        frame_rgb.flags.writeable = True
        
        landmarks = None
        
        if results.multi_hand_landmarks:
            # Extraer landmarks del primer (único) mano
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Convertir landmarks a array de 63 elementos (21 puntos × 3)
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            landmarks = np.array(landmarks, dtype=np.float32)
        
        return landmarks, frame_rgb, results
    
    def draw_landmarks_on_frame(self, frame, results):
        """
        Dibuja los landmarks de la mano en el frame.
        
        Args:
            frame: Imagen BGR
            results: Resultados de MediaPipe
            
        Returns:
            frame: Frame con landmarks dibujados
        """
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.drawing_utils.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.hand_landmarks_style,
                    self.hand_connections_style
                )
        
        return frame
    
    def get_frame_with_landmarks(self, frame):
        """
        Obtiene un frame con los landmarks dibujados y los landmarks extraídos.
        
        Args:
            frame: Imagen BGR
            
        Returns:
            tuple: (landmarks, frame_with_landmarks)
        """
        landmarks, frame_rgb, results = self.extract_landmarks(frame)
        
        # Convertir de vuelta a BGR para dibujar
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        frame_with_landmarks = self.draw_landmarks_on_frame(frame_bgr, results)
        
        return landmarks, frame_with_landmarks
