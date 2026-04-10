"""
Módulo de integración con el bot de Telegram.

Envía mensajes al canal de Telegram con las señas detectadas.
"""

import json
import os
import asyncio
from datetime import datetime

from telegram import Bot
from telegram.error import TelegramError


class TelegramBotManager:
    """
    Gestiona el envío de mensajes a Telegram.
    
    Attributes:
        token (str): Token del bot de Telegram
        chat_id (str): ID del chat/canal
        enabled (bool): Indica si el envío a Telegram está habilitado
        message_format (str): Formato del mensaje (puede incluir {sign} y {confidence})
    """
    
    def __init__(self, config_path=None):
        """
        Inicializa el gestor de Telegram.
        
        Args:
            config_path (str): Ruta al config.json. Si es None, se busca en el directorio raíz.
            
        Raises:
            FileNotFoundError: Si no se encuentra config.json
            ValueError: Si faltan configuraciones críticas en config.json
        """
        if config_path is None:
            # Deducir ruta a partir de este archivo
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config.json")
        
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"No se encontró config.json en {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        telegram_config = config.get("telegram", {})
        
        self.token = telegram_config.get("token", "")
        self.chat_id = telegram_config.get("chat_id", "")
        self.enabled = telegram_config.get("enabled", False)
        self.message_format = telegram_config.get(
            "message_format",
            "✋ Seña detectada: {sign} (confianza: {confidence:.1%})"
        )
        
        # Validaciones
        if not self.token or self.token == "YOUR_BOT_TOKEN_HERE":
            raise ValueError(
                "Token de Telegram no configurado. "
                "Configura 'telegram.token' en config.json"
            )
        
        if not self.chat_id or self.chat_id == "YOUR_CHAT_ID_HERE":
            raise ValueError(
                "Chat ID de Telegram no configurado. "
                "Configura 'telegram.chat_id' en config.json"
            )
        
        self.bot = Bot(token=self.token)
    
    def send_message_async(self, sign, confidence):
        """
        Envía un mensaje a Telegram de forma asincrónica.
        
        Args:
            sign (str): Nombre de la seña detectada
            confidence (float): Confianza de la predicción (0-1)
            
        Returns:
            asyncio.Task: Tarea asincrónica del envío
        """
        if not self.enabled:
            return None
        
        # Formatear mensaje
        message = self.message_format.format(sign=sign, confidence=confidence)
        
        # Crear tarea asincrónica
        return asyncio.create_task(self._send_message_impl(message))
    
    async def _send_message_impl(self, message):
        """Implementación asincrónica del envío."""
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
            return True
        except TelegramError as e:
            print(f"Error enviando mensaje a Telegram: {e}")
            return False
    
    def send_message_sync(self, sign, confidence):
        """
        Envía un mensaje a Telegram de forma síncrona.
        
        Args:
            sign (str): Nombre de la seña detectada
            confidence (float): Confianza de la predicción (0-1)
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        if not self.enabled:
            return False
        
        # Formatear mensaje
        message = self.message_format.format(sign=sign, confidence=confidence)
        
        try:
            # Ejecutar en el event loop (compatible con Tkinter)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.bot.send_message(chat_id=self.chat_id, text=message)
            )
            loop.close()
            return True
        except Exception as e:
            print(f"Error enviando mensaje a Telegram: {e}")
            return False
    
    def set_enabled(self, enabled):
        """Activa/desactiva el envío a Telegram."""
        self.enabled = enabled
    
    def is_enabled(self):
        """Retorna si el envío a Telegram está habilitado."""
        return self.enabled
    
    def set_message_format(self, format_string):
        """
        Configura el formato del mensaje.
        
        Args:
            format_string (str): Formato con placeholders {sign} y {confidence}
        """
        self.message_format = format_string
    
    def get_message_format(self):
        """Retorna el formato actual del mensaje."""
        return self.message_format
    
    def test_connection(self):
        """
        Prueba la conexión con el bot de Telegram.
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Ejecutar en event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Obtener información del bot
            bot_info = loop.run_until_complete(self.bot.get_me())
            loop.close()
            
            return True, f"Conexión exitosa. Bot: @{bot_info.username}"
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"
