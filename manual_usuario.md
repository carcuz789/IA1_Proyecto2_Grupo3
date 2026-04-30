# Manual de Usuario — HandTalk AI

**Versión:** 1.0.0  
**Fecha:** 20 de abril, 2026

---

## 📋 Índice

1. [¿Qué es HandTalk AI?](#qué-es-handtalk-ai)
2. [Instalación Rápida](#instalación-rápida)
3. [Primeros Pasos](#primeros-pasos)
4. [Cómo Usar la Interfaz](#cómo-usar-la-interfaz)
5. [Configurar Telegram](#configurar-telegram)
6. [Panel de Administración](#panel-de-administración)
7. [Preguntas Frecuentes](#preguntas-frecuentes)
8. [Solución de Problemas](#solución-de-problemas)

---

## ¿Qué es HandTalk AI?

**HandTalk AI** es una aplicación que detecta señas manuales en tiempo real usando tu cámara web. Puede reconocer 13 señas diferentes:

- 👋 **hola** — Saludar
- 👋 **bye** — Despedirse
- ✋ **mama** — Madre
- ✋ **papa** — Padre
- 👍 **si** — Afirmación
- 👎 **no** — Negación
- 💧 **agua** — Agua
- 🙏 **gracias** — Agradecimiento
- 🏠 **casa** — Casa
- 🆘 **ayuda** — Solicitud de ayuda
- ✌️ **paz** — Paz
- 🤟 **te_quiero** — Te quiero
- 🤞 **dedo_medio** — Gesto de dedo medio

La aplicación puede enviar automáticamente la seña detectada a un **bot de Telegram** para comunicarse con otros usuarios.

---

## Instalación Rápida

### Opción 1: Instalación Local (Recomendada)

#### En Windows

```bash
# 1. Descargar el proyecto
git clone https://github.com/carcuz789/IA1_Proyecto2_Grupo3.git
cd IA1_Proyecto2_Grupo3

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python app.py
```

#### En macOS

```bash
# 1. Descargar el proyecto
git clone https://github.com/carcuz789/IA1_Proyecto2_Grupo3.git
cd IA1_Proyecto2_Grupo3

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python app.py
```

#### En Linux (Ubuntu/Debian)

```bash
# 1. Instalar Tkinter (requerido)
sudo apt-get install python3-tk

# 2. Descargar proyecto
git clone https://github.com/carcuz789/IA1_Proyecto2_Grupo3.git
cd IA1_Proyecto2_Grupo3

# 3. Instalar dependencias
pip install --user -r requirements.txt

# 4. Ejecutar
python app.py
```

### Opción 2: Instalación con Docker

```bash
# Construir imagen
docker build -t handtalk_ai .

# Ejecutar
docker-compose up
```

---

## Primeros Pasos

### 1. Permitir Acceso a la Cámara

**Windows:** ✓ Automático  
**macOS:** Sistema → Seguridad y privacidad → Cámara → Permitir  
**Linux:** Se requiere permiso de usuario para `/dev/video0`

### 2. Configurar Token de Telegram (Opcional)

Si deseas enviar mensajes a Telegram:

1. Abrir Telegram
2. Buscar usuario `@BotFather`
3. Enviar comando `/newbot`
4. Seguir las instrucciones:
   - Dar nombre al bot (ej: "HandTalkBot")
   - Dar usuario (ej: "my_handtalk_bot")
5. Copiar el **token** que aparece

Con el token:

1. Abrir la aplicación HandTalk AI
2. Presionar botón **⚙️ Panel de Admin**
3. Ir a tab **Telegram**
4. Pegar el token en **"Token del bot"**
5. Presionar **💾 Guardar**

### 3. Primera Ejecución

```bash
python app.py
```

Se abrirá una ventana como esta:

```
┌─────────────────────────────────────────┐
│  HandTalk AI — Sistema de Detección    │
├─────────────────┬──────────────────────┤
│                 │  Seña detectada:     │
│  VIDEO EN       │  ---                 │
│  TIEMPO REAL    │  Confianza: 0%       │
│  (640×480)      │  ████████░░░░░░░░░░  │
│                 │                      │
│                 │  ▶ Iniciar           │
│                 │  ⏹ Detener (disabled)│
│                 │  📱 Enviar (disabled)│
│                 │                      │
│                 │  Estado: Detenido    │
│                 │  Señas: agua, bye... │
└─────────────────┴──────────────────────┘
```

---

## Cómo Usar la Interfaz

### Paso 1: Verificar que la Cámara Inició

Al abrir la app, la cámara **inicia automáticamente**. Verificarás que:
- El video aparece en el recuadro izquierdo
- El estado muestra **"En ejecución"** (verde)
- El botón **▶ Iniciar** aparece deshabilitado
- Los botones **⏹ Detener** y **📱 Enviar** están habilitados

Si necesitas reiniciar la cámara, presiona **⏹ Detener** y luego **▶ Iniciar** manualmente.

### Paso 2: Mostrar una Seña

Colócate frente a la cámara y muestra una seña con la mano:

```
Buen ángulo           Ángulo incorrecto
─────────────         ──────────────────
    ✋                    ←  ✋  →
(mano visible)     (mano parcial/lateral)
```

La aplicación detectará automáticamente la seña:

```
Seña detectada: hola
Confianza: 95%
████████████████░░░ (barra de progreso)
```

### Paso 3: Ajustar el Umbral de Confianza

Si la predicción no es confiable, aumentar el umbral mínimo:

```
Umbral mínimo: 75%  ←--[========░░]--→ 100%
```

- **Umbral bajo (50%):** Detecta más rápido, pero menos preciso
- **Umbral alto (90%):** Detecta más lento, pero más preciso

### Paso 4: Enviar a Telegram (Opcional)

Si la seña tiene suficiente confianza:

1. Presionar botón **📱 Enviar a Telegram**
2. Aparecerá un mensaje: "Mensaje enviado a Telegram: hola (95%)"
3. El mensaje llegará a tu bot de Telegram

### Paso 5: Ver el Historial

Presionar botón **📋 Historial** para ver:

```
┌──────────────────────────────┐
│ HISTORIAL DE MENSAJES        │
├──────────┬────────┬──────────┤
│ Hora     │ Seña   │ Confianza│
├──────────┼────────┼──────────┤
│ 14:30:45 │ hola   │ 95%      │
│ 14:30:52 │ bye    │ 92%      │
│ 14:31:10 │ gracias│ 88%      │
└──────────┴────────┴──────────┘
```

### Paso 6: Detener la Cámara

Presionar botón **⏹ Detener** para:
- Cerrar cámara
- Limpiar video
- Deshabilitar botones

---

## Configurar Telegram

### Crear un Bot

1. **Abrir Telegram**
2. **Buscar:** `@BotFather`
3. **Enviar:** `/newbot`
4. **Responder preguntas:**

```
BotFather: ¿Cómo se llama tu bot?
Respuesta: HandTalkBot

BotFather: ¿Cuál es el nombre de usuario? (debe terminar en 'bot')
Respuesta: my_handtalk_bot

BotFather: ¡Listo! Tu token es:
123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
```

### Obtener tu Chat ID

1. **En Telegram:** Ir a tu bot y enviar `/start`
2. **Abrir navegador:** `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Reemplazar `<TOKEN>` con el token del bot
3. **Copiar:** el número en `"id"`

### Configurar en HandTalk AI

1. **Abrir app:** `python app.py`
2. **Panel de Admin:** ⚙️
3. **Tab Telegram:**
   - Token: `123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh`
   - Chat ID: `987654321`
   - Habilitar Telegram: ✓ marcado
4. **Guardar:** 💾

### Probar Conexión

1. **Presionar:** 🧪 Probar conexión Telegram
2. **Resultado:**
   - ✓ "Conexión exitosa. Bot: @my_handtalk_bot"
   - ✗ "Error de conexión: ..."

---

## Panel de Administración

### Tab 1: Telegram

```
┌─────────────────────────────────┐
│ TELEGRAM                        │
├─────────────────────────────────┤
│                                 │
│ Token del bot:                  │
│ [•••••••••••••••••••••••••••••] │
│                                 │
│ Chat ID:                        │
│ [987654321                     ] │
│                                 │
│ ☑ Habilitar Telegram           │
│                                 │
│ Formato del mensaje:            │
│ ✋ Seña detectada: {sign}       │
│ (confianza: {confidence:.1%})  │
│                                 │
│ Variables: {sign} {confidence}  │
│                                 │
│ [💾 Guardar]                    │
└─────────────────────────────────┘
```

**Opciones:**

| Opción | Uso |
|---|---|
| Token del bot | Token del bot de Telegram |
| Chat ID | ID del chat/usuario destino |
| Habilitar | Activar/desactivar envío a Telegram |
| Formato | Personalizar mensaje enviado |

**Variables disponibles:**

- `{sign}` → Nombre de la seña (ej: "hola")
- `{confidence}` → Confianza decimal (ej: 0.95)
- `{confidence:.1%}` → Confianza % (ej: 95.0%)

### Tab 2: Modelo

```
┌─────────────────────────────────┐
│ MODELO                          │
├─────────────────────────────────┤
│                                 │
│ Umbral de confianza:            │
│ 0%  ←──[════════░░]──→ 100%     │
│         75%                     │
│                                 │
│ [💾 Guardar]                    │
└─────────────────────────────────┘
```

**Umbral:** Confianza mínima para aceptar predicción (0-100%)

### Tab 3: Señas

```
┌─────────────────────────────────┐
│ SEÑAS                           │
├─────────────────────────────────┤
│ Clases disponibles en modelo:   │
│ ┌─────────────────────────────┐ │
│ │ 01. agua                     │ │
│ │ 02. ayuda                    │ │
│ │ 03. bye                      │ │
│ │ 04. casa                     │ │
│ │ 05. dedo_medio               │ │
│ │ 06. gracias                  │ │
│ │ 07. hola                     │ │
│ │ 08. mama  ...                │ │
│ └─────────────────────────────┘ │
│ Total de clases: 13             │
│ ─────────────────────────────── │
│ Señas activas en config.json:   │
│ [agua, ayuda, bye...          ] │
│                                 │
│ [💾 Guardar señas en config]    │
└─────────────────────────────────┘
```

Muestra todas las clases que el modelo puede reconocer y permite editar la lista activa en `config.json`.

### Tab 4: Información

```
┌─────────────────────────────────┐
│ INFORMACIÓN                     │
├─────────────────────────────────┤
│                                 │
│ HandTalk AI — Información       │
│                                 │
│ Modelo:                         │
│   - Ruta: model/model.pkl       │
│   - Algoritmo: SVM (RBF)        │
│   - Accuracy: 100%              │
│                                 │
│ Señas disponibles:              │
│   agua, ayuda, bye, casa, ...   │
│                                 │
│ Cámara:                         │
│   - Device ID: 0                │
│   - Resolución: 640x480         │
│   - FPS: 30                     │
│                                 │
│ Historial:                      │
│   - Habilitado: ✓               │
│   - Mensajes: 5                 │
│                                 │
│ Versión: 1.0.0                 │
│ Fecha: 2026-04-20              │
└─────────────────────────────────┘
```

---

## Preguntas Frecuentes

### P: ¿Funciona sin conexión a internet?

**R:** Sí, la predicción funciona sin internet. Solo necesitas internet si deseas enviar a Telegram.

### P: ¿Puedo usar cualquier cámara web?

**R:** Sí, cualquier cámara USB compatible con OpenCV. En Linux, aparecerá como `/dev/video0` o `/dev/video1`.

### P: ¿Qué pasa si la confianza es baja?

**R:** La seña no se muestra con color. Ajusta:
- Mejorar iluminación
- Mostrar toda la mano
- Reducir el umbral mínimo (con cuidado)

### P: ¿Puedo añadir más señas?

**R:** Sí. El proceso es:
1. Agregar la seña en `config.json` (sección `"signs"`)
2. Ejecutar `python3 data/collect_data.py` y capturar muestras
3. Reentrenar con `python3 model/train.py`
4. Reiniciar la app

### P: ¿Los datos se guardan en línea?

**R:** No. Todo se procesa localmente en tu computadora. El historial se guarda en memoria durante la sesión.

### P: ¿Puedo usar en macOS M1?

**R:** Sí. Python 3.10+ soporta arquitectura ARM64. Instala dependencias con:

```bash
pip install -r requirements.txt --target=$(python -c 'import site; print(site.getsitepackages()[0])') --platform macosx_11_0_arm64
```

### P: ¿Por qué la app es lenta?

**R:** Posibles causas:
- CPU débil o alta carga
- Iluminación insuficiente (MediaPipe invierte más tiempo)
- Resolución muy alta de cámara

Soluciones:
- Cerrar otras aplicaciones
- Mejorar iluminación
- Reducir resolución en configuración (si es posible)

---

## Solución de Problemas

### ❌ "No se pudo abrir la cámara"

**Problema:** La aplicación no accede a la cámara.

**Soluciones:**

1. **Windows:**
   - Verificar permisos: Configuración → Privacidad → Cámara
   - Asegúrate que la app tenga permiso

2. **macOS:**
   - Sistema → Seguridad y privacidad → Cámara
   - Permitir acceso a la app

3. **Linux:**
   ```bash
   # Ver cámaras disponibles
   ls /dev/video*
   
   # Agregar usuario al grupo video
   sudo usermod -a -G video $USER
   
   # Reiniciar sesión o:
   newgrp video
   ```

### ❌ "Tkinter no encontrado"

**Problema:** Import error con Tkinter.

**Soluciones:**

```bash
# Linux (Ubuntu/Debian)
sudo apt-get install python3-tk

# macOS
brew install python-tk@3.10

# Windows (generalmente incluido)
# Si no: reinstalar Python y marcar "tcl/tk"
```

### ❌ "Error al enviar a Telegram"

**Problema:** No se envía el mensaje a Telegram.

**Soluciones:**

1. **Verificar token:**
   - `@BotFather` → `/mybots` → seleccionar bot → `API Token`

2. **Verificar Chat ID:**
   - Enviar mensaje al bot en Telegram
   - Abrir: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Copiar `"id"`

3. **Verificar conexión:**
   - Panel de Admin → 🧪 Probar conexión Telegram
   - Si falla: revisar internet

4. **Verificar permisos:**
   - Estar subscrito/admin en el canal
   - Token correcto

### ❌ "Predicciones incorrectas"

**Problema:** La app detecta señas incorrectas.

**Soluciones:**

1. **Mejorar iluminación:**
   - Aumentar luz ambiente
   - Evitar contraluz

2. **Mostrar seña correctamente:**
   - Mano completa visible
   - Orientación correcta
   - Sin objeto en la mano

3. **Ajustar umbral:**
   - Aumentar a 80-85% para más precisión
   - Reducir a 60-70% para mayor sensibilidad

4. **Entrenar modelo con más datos:**
   - Ejecutar `python data/collect_data.py`
   - Recolectar más muestras
   - Reentrenar con `python model/train.py`

---

## Contacto y Soporte

- **GitHub:** https://github.com/carcuz789/IA1_Proyecto2_Grupo3
- **Issues:** Reportar en: https://github.com/carcuz789/IA1_Proyecto2_Grupo3/issues
- **Email:** Solicitar contacto en GitHub

---

**¡Gracias por usar HandTalk AI!**

Versión 1.0.0 | Grupo 3 — Inteligencia Artificial 1, USAC
