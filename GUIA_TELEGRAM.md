# Guía Completa: Configurar y Probar Telegram con HandTalk AI

## 📱 Paso 1: Crear un Bot de Telegram (Rápido)

### En tu teléfono o PC (Telegram abierto):

1. **Abre Telegram**
2. **Busca:** `@BotFather` (usuario oficial de Telegram)
3. **Envía:** `/newbot`

### BotFather te preguntará:

```
BotFather: 🤖 Alright, a new bot. How should I call it? 
           Please choose a name for your bot.

Tu respuesta: HandTalk Bot
   (o el nombre que quieras)

BotFather: Good. Now let's choose a username for your bot. 
           It must end in 'bot'. Like this, for example: TetrisBot or tetris_bot.

Tu respuesta: mi_handtalk_bot
   (debe terminar en 'bot', usa guiones bajos si es necesario)

BotFather: Done! Congratulations on your new bot. 
           You will find it at t.me/mi_handtalk_bot. 
           You can now add a description, about section and profile picture for your bot, see /help for a list of commands. 
           By the way, when you've finished with your bot, remember that you can always call me if you need to change its name or description.

           Use this token to access the HTTP API:
           123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk
           
           Keep your token secure and store it safely!
```

### 🔑 **Copia y guarda este TOKEN en un lugar seguro:**
```
123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk
```

---

## 🆔 Paso 2: Obtener tu Chat ID

### Opción A: Método Rápido (Recomendado)

1. **En Telegram:** Busca tu bot (ej: `@mi_handtalk_bot`) y envía `/start`

2. **Abre el navegador** y accede a esta URL:
   ```
   https://api.telegram.org/bot123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk/getUpdates
   ```
   
   **Reemplaza:**
   - `123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk` → Tu TOKEN del bot

3. **Busca en el resultado JSON:**
   ```json
   {
     "ok": true,
     "result": [
       {
         "update_id": 123456789,
         "message": {
           "message_id": 1,
           "from": {
             "id": 987654321,    ← ESTE ES TU CHAT ID
             "is_bot": false,
             "first_name": "Josue"
           },
           ...
         }
       }
     ]
   }
   ```

4. **Copia el número en `"id"`:**
   ```
   987654321
   ```

### Opción B: Con Python (Si no funciona lo anterior)

```bash
# Desde la terminal del proyecto:
python << 'EOF'
from src.telegram_bot import TelegramBotManager
# Esto intentará leer getUpdates
import requests
TOKEN = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk"
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates")
data = response.json()
if data['result']:
    chat_id = data['result'][0]['message']['from']['id']
    print(f"Tu Chat ID es: {chat_id}")
else:
    print("No hay mensajes. Envía un mensaje a tu bot primero.")
EOF
```

---

## ⚙️ Paso 3: Configurar en HandTalk AI

### 1. **Ejecuta la aplicación:**
```bash
python app.py
```

### 2. **Abre el Panel de Admin:**
   - Presiona el botón **⚙️ Panel de Admin** en la interfaz

### 3. **Dirígete al tab "Telegram":**
   ```
   ┌─────────────────────────────────┐
   │ TELEGRAM                        │
   ├─────────────────────────────────┤
   │                                 │
   │ Token del bot:                  │
   │ [123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk]
   │                                 │
   │ Chat ID:                        │
   │ [987654321                     ]│
   │                                 │
   │ ☑ Habilitar Telegram           │
   │                                 │
   │ [💾 Guardar]                    │
   └─────────────────────────────────┘
   ```

### 4. **Llena los campos:**
   - **Token del bot:** Pega tu token
   - **Chat ID:** Pega tu chat ID
   - **Habilitar Telegram:** Marca la casilla ✓

### 5. **Presiona "💾 Guardar"**

---

## 🧪 Paso 4: Probar la Conexión

### Opción A: Desde la App (Recomendado)

1. Presiona el botón **🧪 Probar conexión** (si existe en tu versión)
2. O simplemente:
   - Detén la cámara: ⏹️
   - Inicia la cámara: ▶️
   - Muestra una seña
   - Presiona **📱 Enviar a Telegram**
   - **Si funciona:** Verás un mensaje en Telegram del bot

### Opción B: Prueba desde Python

```bash
python << 'EOF'
from src.telegram_bot import TelegramBotManager
from src.admin_panel import AdminPanel

# Cargar configuración
admin = AdminPanel()
token = admin.get_telegram_token()
chat_id = admin.get_telegram_chat_id()

if not token or not chat_id:
    print("❌ Error: Token o Chat ID no configurado")
else:
    try:
        tg = TelegramBotManager()
        # Enviar mensaje de prueba
        message = "✋ Prueba de HandTalk AI - ¡Funciona! 🎉"
        tg.send_message(message)
        print("✅ Mensaje enviado exitosamente a Telegram")
    except Exception as e:
        print(f"❌ Error: {e}")
EOF
```

### Opción C: Prueba Directa con cURL (Terminal)

```bash
# Windows (PowerShell):
$TOKEN = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk"
$CHAT_ID = "987654321"
$MESSAGE = "Hola, esto es una prueba de HandTalk AI"

Invoke-WebRequest -Uri "https://api.telegram.org/bot$TOKEN/sendMessage" `
  -Method Post `
  -Body @{ chat_id = $CHAT_ID; text = $MESSAGE } `
  -ContentType "application/x-www-form-urlencoded"

# Linux/macOS:
TOKEN="123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk"
CHAT_ID="987654321"
MESSAGE="Hola, esto es una prueba de HandTalk AI"

curl -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d chat_id=$CHAT_ID \
  -d text="$MESSAGE" \
  https://api.telegram.org/bot$TOKEN/sendMessage
```

---

## ✅ Solución de Problemas

### ❌ "Token inválido"

```bash
# Verifica que el token sea correcto:
curl https://api.telegram.org/bot{TU_TOKEN}/getMe
```

Si dice `"ok": false`, el token es incorrecto. Vuelve a copiar de @BotFather.

### ❌ "Chat ID inválido"

1. Abre tu bot: `https://t.me/mi_handtalk_bot`
2. Envía `/start`
3. Espera 2 segundos
4. Abre la URL de getUpdates nuevamente en el navegador
5. Busca `"id"` en la respuesta

### ❌ "Error de conexión / Sin internet"

```bash
# Verifica que puedas acceder a internet:
ping 8.8.8.8

# Si está bloqueado, intenta un VPN
```

### ❌ "No recibo mensajes"

1. Verifica que el bot esté **habilitado** en la app (✓ marcado)
2. Verifica que el umbral de confianza no sea muy alto (prueba con 50%)
3. Intenta primero con la "Prueba directa con cURL"

---

## 📤 Paso 5: Usar en Producción

### Una vez que todo funciona:

1. **Muestra una seña** frente a la cámara
2. **Espera** a que la app la detecte (azul = confianza alta)
3. **Presiona:** 📱 **Enviar a Telegram**
4. **Resultado:**
   ```
   Mensaje enviado a Telegram: hola (95%)
   ```
5. **Verifica Telegram** - El bot habrá enviado:
   ```
   ✋ Seña detectada: hola (confianza: 95.0%)
   ```

---

## 🎯 Formato Personalizado

En el panel de admin, puedes personalizar el formato del mensaje:

**Formato por defecto:**
```
✋ Seña detectada: {sign} (confianza: {confidence:.1%})
```

**Ejemplos de formatos:**
```
{sign}: {confidence:.0%}
→ hola: 95%

🎯 {sign} ({confidence})
→ 🎯 hola (0.95)

Seña: {sign}
→ Seña: hola
```

**Variables disponibles:**
- `{sign}` = Nombre de la seña
- `{confidence}` = Confianza decimal (0.0 - 1.0)
- `{confidence:.1%}` = Confianza porcentaje (0.0% - 100.0%)
- `{confidence:.0%}` = Confianza sin decimales (0% - 100%)

---

## 🚀 Resumen Rápido

```
1. @BotFather → /newbot → Copia TOKEN
2. Envía /start a tu bot
3. Abre https://api.telegram.org/botTOKEN/getUpdates → Copia CHAT_ID
4. App → ⚙️ Panel → Telegram → Configura TOKEN + CHAT_ID + ✓ Habilitar
5. Prueba desde la app o con cURL
6. ¡Listo!
```

---

**¿Problemas?** Revisa que:
- ✓ Token es correcto (comienza con números)
- ✓ Chat ID es un número (sin caracteres especiales)
- ✓ Telegram está habilitado en la app
- ✓ La seña tiene confianza > umbral
- ✓ Tienes conexión a internet
