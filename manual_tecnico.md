# Manual Técnico — HandTalk AI

**Versión:** 1.0.0  
**Fecha:** 20 de abril, 2026  
**Autores:** Grupo 3 — Inteligencia Artificial 1, USAC

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Componentes Técnicos](#componentes-técnicos)
4. [Instalación](#instalación)
5. [Configuración](#configuración)
6. [Estructura de Carpetas](#estructura-de-carpetas)
7. [Flujo de Procesamiento](#flujo-de-procesamiento)
8. [API de Módulos](#api-de-módulos)
9. [Problemas Comunes](#problemas-comunes)
10. [Referencias](#referencias)

---

## Descripción General

**HandTalk AI** es un sistema de detección en tiempo real de señas manuales que utiliza técnicas de visión por computadora y aprendizaje automático. El sistema:

- Captura video de la cámara web en tiempo real
- Detecta la mano del usuario utilizando **MediaPipe Hands**
- Extrae 21 puntos de referencia (landmarks) de la mano
- Clasifica la seña utilizando un modelo **SVM** entrenado
- Muestra la predicción y nivel de confianza en una **interfaz gráfica Tkinter**
- Permite enviar el resultado a un **bot de Telegram**

### Especificaciones Clave

| Aspecto | Detalles |
|---|---|
| **Lenguaje** | Python 3.10+ |
| **Señas soportadas** | 10 (agua, ayuda, bye, casa, gracias, hola, mama, no, papa, si) |
| **Dataset** | 1,246 muestras (balance: 108-172 por clase) |
| **Modelo** | SVM (kernel=rbf, C=10, gamma=scale) |
| **Accuracy** | 100% (test), 98.59% ± 0.38% (CV 5-fold) |
| **FPS** | ~30 FPS (en tiempo real) |
| **Resolución** | 640×480 px |

---

## Arquitectura del Sistema

### Diagrama General

```
┌─────────────────────────────────────────────────────────────┐
│                      HANDTALK AI                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              INTERFAZ GRÁFICA (Tkinter)            │   │
│  │  - Mostrar video en tiempo real                    │   │
│  │  - Predicción + confianza                          │   │
│  │  - Botón "Enviar a Telegram"                       │   │
│  │  - Panel de administración                         │   │
│  └─────────────────────────────────────────────────────┘   │
│           │          │              │           │           │
│           ▼          ▼              ▼           ▼           │
│  ┌──────────────┐  ┌──────────┐  ┌─────────┐  ┌─────────┐  │
│  │   CAPTURE    │  │PREDICTOR │  │TELEGRAM │  │ ADMIN   │  │
│  │  (Cámara +   │  │  (SVM +  │  │  (Bot)  │  │ (Config)│  │
│  │  MediaPipe)  │  │  Scaler) │  │         │  │         │  │
│  └──────────────┘  └──────────┘  └─────────┘  └─────────┘  │
│           │          │                │           │         │
│           └──────────┬─────────────────┴───────────┘         │
│                      ▼                                       │
│            ┌──────────────────────┐                          │
│            │    config.json       │                          │
│            │   (Configuración)    │                          │
│            └──────────────────────┘                          │
│                      │                                       │
│            ┌─────────┴────────────┐                          │
│            ▼                      ▼                          │
│        ┌────────────┐      ┌─────────────┐                  │
│        │ model.pkl  │      │ scaler.pkl  │                  │
│        │label_encoder.pkl  │             │                  │
│        └────────────┘      └─────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

```
Cámara
  ↓
┌─ capture.py ────────────────┐
│ OpenCV + MediaPipe          │
│ Captura frame → Detecta mano│
│ Extrae 21 landmarks × 3 = 63│
└──────────┬──────────────────┘
           ↓ (landmarks array)
┌─ predictor.py ──────────────┐
│ Scaler.transform(landmarks) │
│ model.predict() → seña      │
│ Obtiene confianza (0-1)     │
└──────────┬──────────────────┘
           ↓ (predicción + confianza)
┌─ app.py ─────────────────────┐
│ Si confianza > umbral:       │
│  - Mostrar en interfaz       │
│  - Habilitar envío Telegram  │
└──────────┬──────────────────┘
           ↓
┌─ telegram_bot.py ────────────┐
│ Usuario presiona botón        │
│ Envía mensaje a Telegram      │
└──────────────────────────────┘
```

---

## Componentes Técnicos

### 1. **src/capture.py** — Captura de Video y Detección de Mano

**Propósito:** Capturar frames de la cámara web y extraer landmarks de la mano.

**Clase Principal:** `HandCapture`

**Métodos Clave:**

```python
# Abrir/cerrar cámara
capture.open_camera()
capture.close_camera()

# Capturar un frame
frame, success = capture.capture_frame()

# Extraer landmarks (63 valores: 21 puntos × x, y, z)
landmarks, frame_rgb, results = capture.extract_landmarks(frame)

# Dibujar landmarks en el frame
frame = capture.draw_landmarks_on_frame(frame, results)

# Obtener frame con landmarks dibujados
landmarks, frame_with_landmarks = capture.get_frame_with_landmarks(frame)
```

**Tecnologías Utilizadas:**

- **OpenCV 4.9.0:** Captura de video (`cv2.VideoCapture`)
- **MediaPipe 0.10.9:** Detección de manos (`mp.solutions.hands`)

**Configuración:**

```python
HandCapture(device_id=0)  # 0 = cámara por defecto
# Resolución: 640×480
# FPS: 30
# Confianza mínima: 50%
```

---

### 2. **src/predictor.py** — Clasificación de Señas

**Propósito:** Cargar el modelo entrenado y realizar predicciones.

**Clase Principal:** `SignPredictor`

**Métodos Clave:**

```python
# Inicializar (carga automáticamente model.pkl, scaler.pkl, label_encoder.pkl)
predictor = SignPredictor(base_dir="/ruta/al/proyecto")

# Predecir
prediction = predictor.predict(landmarks)  # Array (63,)
# Retorna: {
#    'sign': 'hola',
#    'confidence': 0.95,
#    'all_probabilities': {'hola': 0.95, 'bye': 0.03, ...}
# }

# Verificar si es confiable
is_confident = predictor.is_confident(prediction, threshold=0.75)

# Obtener lista de señas
signs = predictor.get_available_signs()  # ['agua', 'hola', ...]
```

**Modelo Machine Learning:**

- **Algoritmo:** Support Vector Machine (SVM)
- **Kernel:** RBF (Radial Basis Function)
- **Parámetros:** C=10, gamma=scale, probability=True
- **Preprocesamiento:** StandardScaler (normalización Z-score)
- **Codificación de etiquetas:** LabelEncoder

**Rendimiento:**

| Métrica | Valor |
|---|---|
| Test Accuracy | 100% |
| CV 5-fold | 98.59% ± 0.38% |
| Precisión ponderada | 100% |
| Recall ponderado | 100% |

---

### 3. **src/telegram_bot.py** — Integración con Telegram

**Propósito:** Enviar mensajes a Telegram con las señas detectadas.

**Clase Principal:** `TelegramBotManager`

**Métodos Clave:**

```python
# Inicializar (lee config.json)
telegram = TelegramBotManager(config_path="/ruta/config.json")

# Enviar mensaje síncrono
success = telegram.send_message_sync(sign="hola", confidence=0.95)

# Enviar mensaje asincrónico (para no bloquear UI)
task = telegram.send_message_async(sign="hola", confidence=0.95)

# Probar conexión
success, message = telegram.test_connection()

# Activar/desactivar
telegram.set_enabled(True)
is_enabled = telegram.is_enabled()
```

**Configuración en `config.json`:**

```json
{
  "telegram": {
    "token": "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh",
    "chat_id": "987654321",
    "enabled": true,
    "message_format": "✋ Seña detectada: {sign} (confianza: {confidence:.1%})"
  }
}
```

**Parámetros del Mensaje:**

- `{sign}` — Nombre de la seña detectada (ej: "hola")
- `{confidence}` — Confianza como decimal (ej: 0.95)
- `{confidence:.1%}` — Confianza como porcentaje (ej: 95.0%)

**Creación del Bot de Telegram:**

1. Abrir Telegram → buscar `@BotFather`
2. Comando: `/newbot`
3. Dar nombre y usuario del bot
4. Copiar token → guardar en `config.json`
5. Obtener chat_id: enviar `/start` al bot y revisar updates

---

### 4. **src/admin_panel.py** — Administración de Configuración

**Propósito:** Gestionar la configuración central del sistema.

**Clase Principal:** `AdminPanel`

**Métodos Clave:**

```python
# Inicializar
admin = AdminPanel(config_path="/ruta/config.json")

# Umbral de confianza
threshold = admin.get_confidence_threshold()  # 0.75
admin.set_confidence_threshold(0.85)

# Telegram
token = admin.get_telegram_token()
admin.set_telegram_token("nuevo_token")
admin.set_telegram_enabled(True)

# Señas
signs = admin.get_available_signs()  # ['agua', 'hola', ...]
admin.set_available_signs(['agua', 'bye', 'casa'])

# Cámara
device_id = admin.get_camera_device_id()  # 0
admin.set_camera_device_id(1)

# Historial
is_enabled = admin.is_history_enabled()
admin.set_history_enabled(False)

# Mostrar resumen
admin.print_summary()
```

---

### 5. **app.py** — Interfaz Gráfica Principal

**Propósito:** Interfaz gráfica que integra todos los módulos.

**Componentes:**

- **Canvas de video:** Muestra frames en tiempo real
- **Etiquetas de predicción:** Seña + confianza + barra de progreso
- **Control de umbral:** Slider para ajustar confianza mínima
- **Botones de control:** Iniciar/Detener cámara, Enviar a Telegram
- **Panel de administración:** Configuración de Telegram, modelo, etc.
- **Historial:** Registro de mensajes enviados
- **Información:** Lista de señas disponibles, estado del sistema

**Thread de Captura:**

```
Hilo principal (Tkinter loop)
    ↑
    │ self.window.after()  ← actualizar UI
    │
Hilo secundario (capture loop)
    ├─ Capturar frame
    ├─ Extraer landmarks
    ├─ Predecir
    └─ Dibujar en frame
    (Loop cada ~33ms para 30 FPS)
```

**Flujo de Predicción en Tiempo Real:**

```
1. Usuario presiona "Iniciar"
2. Abrir cámara → iniciar thread de captura
3. En cada frame:
   a. Capturar → extraer landmarks
   b. Predecir → obtener seña + confianza
   c. Si confianza > umbral:
      - Mostrar en interfaz
      - Habilitar botón "Enviar a Telegram"
   d. Dibujar landmarks en frame
   e. Convertir BGR→RGB→PIL→ImageTk
   f. Mostrar en canvas
4. Usuario presiona botón → enviar a Telegram
5. Grabar en historial
6. Usuario presiona "Detener" → cerrar cámara, detener thread
```

---

## Instalación

### Requisitos del Sistema

- **OS:** Linux (Ubuntu 20.04+) / macOS / Windows 10+
- **Python:** 3.10+
- **Cámara:** Conectada y accesible en `/dev/video0` (Linux)
- **Tkinter:** Instalado (generalmente incluido en Python, excepto en Linux)

### En Linux (Ubuntu/Debian)

```bash
# Clonar repositorio
git clone https://github.com/carcuz789/IA1_Proyecto2_Grupo3.git
cd IA1_Proyecto2_Grupo3

# Instalar Tkinter (requerido)
sudo apt-get install python3-tk

# Instalar dependencias Python
pip install --user -r requirements.txt

# Entrenar el modelo (si no existe model/model.pkl)
python model/train.py

# Ejecutar la aplicación
python app.py
```

### En macOS

```bash
# Clonar repositorio
git clone https://github.com/carcuz789/IA1_Proyecto2_Grupo3.git
cd IA1_Proyecto2_Grupo3

# Instalar dependencias (Tkinter incluido en Python)
pip install -r requirements.txt

# Entrenar modelo
python model/train.py

# Ejecutar
python app.py
```

### En Windows

```bash
# Clonar repositorio (usar Git Bash o PowerShell)
git clone https://github.com/carcuz789/IA1_Proyecto2_Grupo3.git
cd IA1_Proyecto2_Grupo3

# Instalar dependencias
pip install -r requirements.txt

# Entrenar modelo
python model/train.py

# Ejecutar
python app.py
```

### Con Docker

```bash
# Construir imagen
docker build -t handtalk_ai .

# Ejecutar con docker-compose (requiere acceso a display)
docker-compose up
```

---

## Configuración

### config.json

```json
{
  "telegram": {
    "token": "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh",
    "chat_id": "987654321",
    "enabled": true,
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
  "history_enabled": true
}
```

### Variables de Configuración

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `telegram.token` | Token del bot de Telegram | Debe ser configurado |
| `telegram.chat_id` | ID del chat/canal de Telegram | Debe ser configurado |
| `telegram.enabled` | Habilitar/desabilitar Telegram | `true` |
| `telegram.message_format` | Formato del mensaje | `"✋ Seña detectada: {sign} (confianza: {confidence:.1%})"` |
| `model.confidence_threshold` | Confianza mínima (0-1) | `0.75` (75%) |
| `camera.device_id` | ID del dispositivo de cámara | `0` |
| `history_enabled` | Guardar historial de mensajes | `true` |

---

## Estructura de Carpetas

```
IA1_Proyecto2_Grupo3/
├── app.py                           # Interfaz principal (Tkinter)
├── config.json                      # Configuración central
├── requirements.txt                 # Dependencias Python
├── Dockerfile                       # Definición de imagen Docker
├── docker-compose.yml               # Orquestación de contenedores
├── README.md                        # Documentación del proyecto
├── manual_tecnico.md               # Este archivo
├── manual_usuario.md               # Guía para usuarios finales
│
├── data/                            # Dataset
│   ├── raw/                         # Imágenes/videos crudos
│   ├── processed/
│   │   └── dataset.csv             # 1,246 muestras, 63 features + label
│   └── collect_data.py             # Script de recolección
│
├── model/                           # Modelo de ML
│   ├── train.py                     # Script de entrenamiento
│   ├── model.pkl                    # Modelo SVM (gitignore)
│   ├── scaler.pkl                   # StandardScaler (gitignore)
│   ├── label_encoder.pkl            # LabelEncoder (gitignore)
│   └── results/                     # Matrices de confusión (gitignore)
│       ├── confusion_KNN.png
│       ├── confusion_SVM.png
│       ├── confusion_Random_Forest.png
│       ├── confusion_Logistic_Regression.png
│       └── comparacion_algoritmos.png
│
└── src/                             # Módulos del sistema
    ├── capture.py                   # Captura de video + MediaPipe
    ├── predictor.py                 # Predictor del modelo
    ├── telegram_bot.py              # Bot de Telegram
    └── admin_panel.py               # Panel administrativo
```

### Archivos .gitignore

```
# Dataset (muy grande)
data/raw/
data/processed/dataset.csv

# Modelos entrenados (binarios)
model/model.pkl
model/scaler.pkl
model/label_encoder.pkl
model/results/

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Sistema
.DS_Store
Thumbs.db
```

---

## Flujo de Procesamiento

### Flujo Completo de Predicción (30 FPS)

**Tiempo total por frame:** ~33 ms

```
Frame n
├─ [~3ms]   Capturar de cámara (OpenCV)
├─ [~8ms]   Detectar mano (MediaPipe Hands)
│           - Inicializa red neural convolucional
│           - Detecta presencia de mano
│           - Extrae 21 landmarks (x, y, z)
├─ [~1ms]   Normalizar con scaler
├─ [~2ms]   Predecir con SVM
│           - Transforma a espacio RBF
│           - Calcula distancia a hiperplano
│           - Obtiene probabilidades
├─ [~5ms]   Dibujar en frame (OpenCV)
│           - Dibuja conexiones de landmarks
│           - Dibuja puntos
│           - Agrega texto de predicción
├─ [~10ms]  Convertir BGR→RGB→PIL→ImageTk
│           - Conversión de espacio de color
│           - Redimensionamiento (640×480)
│           - Codificación PNG
├─ [~3ms]   Actualizar UI (Tkinter)
│           - Canvas.create_image()
│           - Label.config()
│           - Progressbar.config()
└─ [~1ms]   Buffer y sincronización
```

**Punto de decisión para Telegram:**

```
Si confianza > umbral_minimo:
    ├─ Mostrar en interfaz ✓
    ├─ Habilitar botón ✓
    └─ Usuario presiona → send_message_sync() [~500ms]
        ├─ Preparar JSON
        ├─ HTTPS POST a Telegram API
        ├─ Grabar en historial
        └─ Mostrar confirmación
```

---

## API de Módulos

### src.capture.HandCapture

```python
class HandCapture:
    def __init__(self, device_id=0)
    def open_camera(self)
    def close_camera(self)
    def capture_frame(self) -> (frame, success)
    def extract_landmarks(frame) -> (landmarks, frame_rgb, results)
    def draw_landmarks_on_frame(frame, results) -> frame
    def get_frame_with_landmarks(frame) -> (landmarks, frame_with_landmarks)
```

### src.predictor.SignPredictor

```python
class SignPredictor:
    def __init__(self, base_dir=None)
    def predict(landmarks) -> dict | None
    def get_available_signs() -> list
    def is_confident(prediction, threshold) -> bool
```

### src.telegram_bot.TelegramBotManager

```python
class TelegramBotManager:
    def __init__(self, config_path=None)
    def send_message_sync(sign, confidence) -> bool
    def send_message_async(sign, confidence) -> asyncio.Task
    def set_enabled(enabled)
    def is_enabled() -> bool
    def test_connection() -> (success, message)
```

### src.admin_panel.AdminPanel

```python
class AdminPanel:
    def __init__(self, config_path=None)
    def load_config()
    def save_config()
    def get/set_confidence_threshold(threshold)
    def get/set_telegram_token(token)
    def get/set_telegram_chat_id(chat_id)
    def get/set_available_signs(signs)
    def print_summary()
```

---

## Problemas Comunes

### 1. "No se pudo abrir la cámara"

**Causa:** La cámara no es accesible.

**Solución:**

```bash
# Linux: Verificar permisos
ls -l /dev/video*
sudo usermod -a -G video $USER
# Reiniciar sesión

# macOS: Permitir acceso en Preferencias → Seguridad

# Windows: Verificar en Administrador de dispositivos
```

### 2. "ModuleNotFoundError: No module named 'mediapipe'"

**Causa:** Dependencias no instaladas.

**Solución:**

```bash
pip install --user -r requirements.txt
# Si persiste:
pip install mediapipe==0.10.9 --no-cache-dir
```

### 3. "Tkinter not found / ImportError: _tkinter.TclError"

**Causa:** Tkinter no instalado.

**Solución:**

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (incluido en Python)
# Windows (incluido en Python)

# Si sigue fallando:
brew install python-tk@3.10  # macOS
```

### 4. "ERROR: Telegram connection failed"

**Causa:** Token o chat_id incorrecto.

**Solución:**

1. Verificar token: `@BotFather` → `/mybots` → seleccionar bot → `API Token`
2. Verificar chat_id: enviar mensaje al bot → ir a `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Actualizar `config.json`
4. Usar botón "🧪 Probar conexión Telegram" en la interfaz

### 5. "cv2.imshow() doesn't work en Wayland"

**Nota:** Esto ya está solucionado usando Tkinter en lugar de cv2.imshow().

**Si ocurre en otro contexto:**

```bash
export GDK_BACKEND=x11  # Forzar X11 si es necesario
python app.py
```

### 6. "Model.pkl not found"

**Causa:** El modelo no está entrenado.

**Solución:**

```bash
# Entrenar modelo
python model/train.py

# Verifica que exista: data/processed/dataset.csv
ls -la data/processed/dataset.csv
```

### 7. "Baja precisión / predicciones incorrectas"

**Causas posibles:**

- Iluminación insuficiente
- Ángulo de mano incorrecto
- Mano parcialmente fuera del frame
- Umbral de confianza muy bajo

**Soluciones:**

1. Aumentar iluminación
2. Mostrar toda la mano en el frame
3. Ajustar umbral mínimo en panel de admin (↑ a 0.80)
4. Volver a entrenar modelo con más datos

---

## Referencias

### Librerías Utilizadas

- **OpenCV 4.9.0:** https://opencv.org/
- **MediaPipe 0.10.9:** https://mediapipe.dev/
- **scikit-learn 1.4.2:** https://scikit-learn.org/
- **python-telegram-bot 20.8:** https://python-telegram-bot.org/
- **Tkinter:** https://docs.python.org/3/library/tkinter.html
- **PIL (Pillow):** https://python-pillow.org/

### Documentación

- [MediaPipe Hands](https://mediapipe.dev/solutions/hands)
- [OpenCV Tutorials](https://docs.opencv.org/)
- [scikit-learn SVM](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
- [Telegram Bot API](https://core.telegram.org/bots/api)

### Papers Relacionados

- Handpose Estimation Using MediaPipe
- Support Vector Machines for Real-time Classification
- Real-time Hand Pose Estimation from Monocular RGB Images

---

**Versión:** 1.0.0 | **Última actualización:** 20/04/2026  
**Grupo 3 — Inteligencia Artificial 1, USAC**
