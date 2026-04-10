"""
Módulo administrativo para configuración del sistema.

Permite configurar umbral de confianza, format de mensaje, lista de señas, etc.
"""

import json
import os


class AdminPanel:
    """
    Gestiona la configuración del sistema.
    
    Attributes:
        config_path (str): Ruta al config.json
        config (dict): Configuración cargada
    """
    
    def __init__(self, config_path=None):
        """
        Inicializa el panel de administración.
        
        Args:
            config_path (str): Ruta al config.json
            
        Raises:
            FileNotFoundError: Si no se encuentra config.json
        """
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config.json")
        
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"No se encontró config.json en {config_path}")
        
        self.config_path = config_path
        self.load_config()
    
    def load_config(self):
        """Carga la configuración desde config.json."""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
    
    def save_config(self):
        """Guarda la configuración en config.json."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    # ── Métodos para configuración de Telegram ──────────────────────────────
    
    def get_telegram_token(self):
        """Retorna el token de Telegram."""
        return self.config.get("telegram", {}).get("token", "")
    
    def set_telegram_token(self, token):
        """Configura el token de Telegram."""
        if "telegram" not in self.config:
            self.config["telegram"] = {}
        self.config["telegram"]["token"] = token
        self.save_config()
    
    def get_telegram_chat_id(self):
        """Retorna el chat_id de Telegram."""
        return self.config.get("telegram", {}).get("chat_id", "")
    
    def set_telegram_chat_id(self, chat_id):
        """Configura el chat_id de Telegram."""
        if "telegram" not in self.config:
            self.config["telegram"] = {}
        self.config["telegram"]["chat_id"] = str(chat_id)
        self.save_config()
    
    def is_telegram_enabled(self):
        """Retorna si Telegram está habilitado."""
        return self.config.get("telegram", {}).get("enabled", False)
    
    def set_telegram_enabled(self, enabled):
        """Activa/desactiva Telegram."""
        if "telegram" not in self.config:
            self.config["telegram"] = {}
        self.config["telegram"]["enabled"] = bool(enabled)
        self.save_config()
    
    def get_telegram_message_format(self):
        """Retorna el formato del mensaje de Telegram."""
        return self.config.get("telegram", {}).get(
            "message_format",
            "✋ Seña detectada: {sign} (confianza: {confidence:.1%})"
        )
    
    def set_telegram_message_format(self, format_string):
        """Configura el formato del mensaje de Telegram."""
        if "telegram" not in self.config:
            self.config["telegram"] = {}
        self.config["telegram"]["message_format"] = format_string
        self.save_config()
    
    # ── Métodos para configuración del modelo ──────────────────────────────
    
    def get_confidence_threshold(self):
        """Retorna el umbral de confianza."""
        return self.config.get("model", {}).get("confidence_threshold", 0.75)
    
    def set_confidence_threshold(self, threshold):
        """
        Configura el umbral de confianza.
        
        Args:
            threshold (float): Valor entre 0 y 1
        """
        threshold = float(threshold)
        if not (0 <= threshold <= 1):
            raise ValueError("El umbral debe estar entre 0 y 1")
        
        if "model" not in self.config:
            self.config["model"] = {}
        self.config["model"]["confidence_threshold"] = threshold
        self.save_config()
    
    def get_model_path(self):
        """Retorna la ruta del modelo."""
        return self.config.get("model", {}).get("path", "model/model.pkl")
    
    # ── Métodos para señas ─────────────────────────────────────────────────
    
    def get_available_signs(self):
        """Retorna la lista de señas disponibles."""
        return self.config.get("signs", [])
    
    def set_available_signs(self, signs):
        """Configura la lista de señas disponibles."""
        self.config["signs"] = list(signs)
        self.save_config()
    
    # ── Métodos para cámara ────────────────────────────────────────────────
    
    def get_camera_device_id(self):
        """Retorna el ID del dispositivo de cámara."""
        return self.config.get("camera", {}).get("device_id", 0)
    
    def set_camera_device_id(self, device_id):
        """Configura el ID del dispositivo de cámara."""
        if "camera" not in self.config:
            self.config["camera"] = {}
        self.config["camera"]["device_id"] = int(device_id)
        self.save_config()
    
    # ── Métodos para historial ─────────────────────────────────────────────
    
    def is_history_enabled(self):
        """Retorna si el historial está habilitado."""
        return self.config.get("history_enabled", True)
    
    def set_history_enabled(self, enabled):
        """Activa/desactiva el historial."""
        self.config["history_enabled"] = bool(enabled)
        self.save_config()
    
    # ── Métodos generales ───────────────────────────────────────────────────
    
    def get_config(self):
        """Retorna la configuración completa."""
        return self.config.copy()
    
    def reset_config(self):
        """
        Reinicia la configuración a valores por defecto.
        
        Preserva el token de Telegram si existe.
        """
        token = self.get_telegram_token()
        chat_id = self.get_telegram_chat_id()
        
        self.config = {
            "telegram": {
                "token": token,
                "chat_id": chat_id,
                "enabled": True,
                "message_format": "✋ Seña detectada: {sign} (confianza: {confidence:.1%})"
            },
            "model": {
                "path": "model/model.pkl",
                "confidence_threshold": 0.75
            },
            "signs": ["agua", "ayuda", "bye", "casa", "gracias", "hola", "mama", "no", "papa", "si"],
            "camera": {
                "device_id": 0
            },
            "history_enabled": True
        }
        self.save_config()
    
    def print_summary(self):
        """Imprime un resumen de la configuración actual."""
        print("\n" + "="*60)
        print("Configuración del Sistema — HandTalk AI")
        print("="*60)
        
        print("\nTelegram:")
        print(f"  Habilitado: {self.is_telegram_enabled()}")
        print(f"  Token: {self.get_telegram_token()[:10]}..." if self.get_telegram_token() else "  Token: NO CONFIGURADO")
        print(f"  Chat ID: {self.get_telegram_chat_id()}")
        
        print("\nModelo:")
        print(f"  Confianza mínima: {self.get_confidence_threshold():.0%}")
        
        print("\nCámara:")
        print(f"  Device ID: {self.get_camera_device_id()}")
        
        print("\nSeñas disponibles:")
        for i, sign in enumerate(self.get_available_signs(), 1):
            print(f"  {i:2}. {sign}")
        
        print("\nHistorial:")
        print(f"  Habilitado: {self.is_history_enabled()}")
        print("="*60 + "\n")
