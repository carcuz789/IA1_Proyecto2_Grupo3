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
            
        # NOTA: Ya no instanciamos self.bot globalmente aquí 
        # para evitar fugas de memoria y conexiones abiertas.

    def send_message_async(self, sign, confidence):
        """
        Envía un mensaje a Telegram de forma asincrónica.
        """
        if not self.enabled:
            return None
        
        # Formatear mensaje
        message = self.message_format.format(sign=sign, confidence=confidence)
        
        # Crear tarea asincrónica
        return asyncio.create_task(self._send_message_impl(message))
    
    async def _send_message_impl(self, message):
        """Implementación asincrónica del envío que cierra su propia conexión."""
        try:
            # Usar async with asegura que el pool de conexiones se cierre
            async with Bot(token=self.token) as bot:
                await bot.send_message(chat_id=self.chat_id, text=message)
                return True
        except TelegramError as e:
            print(f"Error enviando mensaje a Telegram: {e}")
            return False
    
    def send_message_sync(self, sign, confidence):
        """
        Envía un mensaje a Telegram de forma síncrona limpiamente.
        """
        if not self.enabled:
            return False
        
        message = self.message_format.format(sign=sign, confidence=confidence)
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # Llamamos a _send_message_impl que maneja su propio cierre de bot
            result = loop.run_until_complete(self._send_message_impl(message))
            loop.close()
            return result
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
        """Configura el formato del mensaje."""
        self.message_format = format_string
    
    def get_message_format(self):
        """Retorna el formato actual del mensaje."""
        return self.message_format
    
    def test_connection(self):
        """
        Prueba la conexión con el bot de Telegram.
        """
        async def _test():
            # async with cierra la conexión al terminar la prueba
            async with Bot(token=self.token) as bot:
                return await bot.get_me()

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            bot_info = loop.run_until_complete(_test())
            loop.close()
            
            return True, f"Conexión exitosa. Bot: @{bot_info.username}"
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"