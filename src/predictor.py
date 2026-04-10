"""
Módulo predictor de señas usando el modelo entrenado.

Carga el modelo, scaler y label encoder, y realiza predicciones
sobre los landmarks extraídos.
"""

import os
import sys

import joblib
import numpy as np


class SignPredictor:
    """
    Predice la seña basada en los landmarks de la mano.
    
    Attributes:
        model: Modelo SVM entrenado
        scaler: StandardScaler para normalizar features
        label_encoder: LabelEncoder para decodificar predicciones
    """
    
    def __init__(self, base_dir=None):
        """
        Inicializa el predictor cargando el modelo entrenado.
        
        Args:
            base_dir (str): Directorio base del proyecto. Si es None, se deduce automáticamente.
            
        Raises:
            FileNotFoundError: Si no se encuentra alguno de los archivos del modelo.
        """
        if base_dir is None:
            # Deducir base_dir a partir de la ubicación de este script
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.base_dir = base_dir
        
        # Rutas de los archivos del modelo
        model_path = os.path.join(base_dir, "model", "model.pkl")
        scaler_path = os.path.join(base_dir, "model", "scaler.pkl")
        encoder_path = os.path.join(base_dir, "model", "label_encoder.pkl")
        
        # Verificar que todos los archivos existen
        for path, name in [(model_path, "model.pkl"), 
                          (scaler_path, "scaler.pkl"), 
                          (encoder_path, "label_encoder.pkl")]:
            if not os.path.isfile(path):
                raise FileNotFoundError(
                    f"No se encontró {name} en {path}\n"
                    f"Ejecuta primero: python model/train.py"
                )
        
        # Cargar modelo, scaler y encoder
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.label_encoder = joblib.load(encoder_path)
        
        # Lista de señas disponibles
        self.signs = list(self.label_encoder.classes_)
    
    def predict(self, landmarks):
        """
        Predice la seña basada en los landmarks.
        
        Args:
            landmarks (np.ndarray): Array de forma (63,) con los landmarks de la mano
            
        Returns:
            dict: {
                'sign': str - nombre de la seña predicha,
                'confidence': float - confianza de la predicción (0-1),
                'all_probabilities': dict - probabilidades para todas las clases
            }
            
        Returns None si los landmarks son None.
        """
        if landmarks is None:
            return None
        
        # Asegurar que es un array de forma (1, 63)
        landmarks = np.array(landmarks).reshape(1, -1)
        
        # Escalar usando el scaler entrenado
        landmarks_scaled = self.scaler.transform(landmarks)
        
        # Predecir
        prediction = self.model.predict(landmarks_scaled)[0]
        
        # Obtener confianza (probabilidades)
        probabilities = self.model.predict_proba(landmarks_scaled)[0]
        
        # Decodificar la predicción
        sign = self.label_encoder.inverse_transform([prediction])[0]
        confidence = float(max(probabilities))
        
        # Crear diccionario de probabilidades para todas las clases
        all_probs = {
            sign: float(prob) 
            for sign, prob in zip(self.label_encoder.classes_, probabilities)
        }
        
        return {
            'sign': sign,
            'confidence': confidence,
            'all_probabilities': all_probs
        }
    
    def get_available_signs(self):
        """
        Retorna la lista de señas disponibles.
        
        Returns:
            list: Lista de nombres de señas
        """
        return self.signs
    
    def is_confident(self, prediction, threshold):
        """
        Verifica si la predicción supera el umbral de confianza.
        
        Args:
            prediction (dict): Resultado de predict()
            threshold (float): Umbral de confianza (0-1)
            
        Returns:
            bool: True si la confianza >= threshold
        """
        if prediction is None:
            return False
        return prediction['confidence'] >= threshold
