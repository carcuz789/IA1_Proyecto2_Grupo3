# HandTalk AI — Contexto del Proyecto para el Asistente

## Información General
- **Curso:** Inteligencia Artificial 1 — Universidad San Carlos de Guatemala, Facultad de Ingeniería
- **Proyecto:** Proyecto 2 — HandTalk AI
- **Ponderación:** 40 puntos (~50 horas de trabajo)
- **Grupo:** Grupo 3
- **Integrantes activos programando:** 2 personas

## Repositorio GitHub
- **URL:** https://github.com/carcuz789/IA1_Proyecto2_Grupo3
- **Dueño (cuenta GitHub):** `carcuz789`
- **Colaborador del equipo:** `JosueC23` (permisos de escritura/push)
- **Auxiliares obligatorios agregados:**
  - `roberto1206` (permisos de lectura)
  - `ixchop98` (permisos de lectura)
- **Nota:** El nombre requerido en el enunciado es `IA1_1S2026_G03_Proyecto2`. El repositorio fue creado como `IA1_Proyecto2_Grupo3`. Se puede renombrar si el auxiliar lo exige.

## Fechas Clave
| Entrega | Fecha límite | Estado |
|---|---|---|
| Entrega 1 — Tarea 2 (avance básico) | 09/04/2026 | ⚠️ Ya venció |
| **Entrega Final — Proyecto completo** | **01/05/2026** | 🔴 Pendiente |
| Calificación | 02/05/2026 | — |

> Quedan aproximadamente **21 días** para la entrega final (desde el 10/04/2026).

---

## Descripción del Sistema a Construir

Sistema que:
1. Captura video en tiempo real desde la cámara web
2. Detecta la mano del usuario con **MediaPipe Hands + OpenCV**
3. Extrae landmarks (21 puntos de la mano) como features
4. Clasifica la seña con un modelo de **Machine Learning** (scikit-learn)
5. Muestra la predicción + nivel de confianza en una **interfaz gráfica**
6. Permite **enviar el mensaje a un bot de Telegram** con un botón

---

## Arquitectura del Proyecto

```
IA_P2/
├── data/                        # Dataset recolectado por el equipo
│   ├── raw/                     # Imágenes/videos crudos por clase
│   └── processed/               # Features extraídas (CSV o numpy)
├── model/
│   ├── train.py                 # Script de entrenamiento
│   ├── evaluate.py              # Evaluación del modelo
│   └── model.pkl                # Modelo entrenado guardado
├── src/
│   ├── capture.py               # Captura de video + extracción de landmarks
│   ├── predictor.py             # Carga modelo y predice en tiempo real
│   ├── telegram_bot.py          # Integración con bot de Telegram
│   └── admin_panel.py           # Módulo administrativo
├── app.py                       # Punto de entrada principal (interfaz gráfica)
├── config.json                  # Configuración del sistema (umbral, token, etc.)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── manual_tecnico.md
└── manual_usuario.md
```

---

## Módulos del Sistema

### Módulo Principal (obligatorio)
- Captura de video en tiempo real
- Detección de mano con MediaPipe Hands
- Extracción de 21 landmarks (x, y, z) = 63 features por frame
- Clasificación con modelo scikit-learn
- Interfaz gráfica que muestra: palabra detectada + % confianza
- Botón "Enviar a Telegram"

### Módulo Administrativo (obligatorio)
- Configurar **umbral de confianza** para aceptar predicción
- Ver lista de señas disponibles
- Definir/modificar el **formato del mensaje** de Telegram
- Activar/desactivar envío a Telegram
- (Opcional) Historial de mensajes enviados

---

## Stack Tecnológico
| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.10+ |
| Computer Vision | OpenCV 4.9.0, MediaPipe 0.10.9 |
| Machine Learning | scikit-learn 1.4.2 |
| Algoritmos probados | KNN, SVM ✅, Random Forest, Logistic Regression |
| Interfaz gráfica | **Tkinter** (se eligió porque PyQt5 tiene problemas en Wayland) |
| Mensajería | python-telegram-bot 20.8 |
| Despliegue | Docker + docker-compose |
| Gestión de entorno | sistema (sin venv — instalación con pip --user) |

### Notas críticas de instalación
- **NO usar mediapipe >= 0.10.10** — arrastra `torch` + `triton` + nvidia drivers (>700MB). Usar `mediapipe==0.10.9`
- **Tkinter** no se instala con pip: `sudo apt install python3-tk`
- **El sistema usa Wayland** (Ubuntu 22.04). `cv2.imshow` NO funciona en Wayland. Toda UI debe usar **Tkinter**
- La webcam es `USB2.0 VGA UVC WebCam` en `/dev/video0` y `/dev/video1` (par, usar device_id=0)
- Para mostrar video en Tkinter: convertir frame BGR→RGB → `PIL.Image` → `ImageTk.PhotoImage`

---

## Dataset ✅ COMPLETADO
- **Archivo:** `data/processed/dataset.csv`
- **Total muestras:** 1246
- **Script de recolección:** `data/collect_data.py` (usa Tkinter para display)
- **Features:** 63 columnas (21 landmarks × x, y, z) + columna `label`
- **Clases y muestras:**

| Seña | Muestras |
|---|---|
| agua | 129 |
| ayuda | 117 |
| bye | 122 |
| casa | 118 |
| gracias | 116 |
| hola | 109 |
| mama | 172 |
| no | 138 |
| papa | 117 |
| si | 108 |

> El dataset NO se versiona en git (está en .gitignore). Cada integrante debe tenerlo localmente.

---

## Modelo de Machine Learning ✅ COMPLETADO
- **Script:** `model/train.py`
- **Modelo elegido:** SVM (kernel=rbf, C=10, gamma=scale)
- **Archivos generados** (en .gitignore, no se suben al repo):
  - `model/model.pkl` — modelo entrenado
  - `model/scaler.pkl` — StandardScaler
  - `model/label_encoder.pkl` — LabelEncoder
  - `model/results/` — matrices de confusión + gráfica comparativa

### Resultados de evaluación
| Algoritmo | Test Accuracy | CV 5-fold |
|---|---|---|
| **SVM** ✅ | **100%** | 98.59% ± 0.38% |
| Random Forest | 100% | 99.00% ± 0.32% |
| KNN | 98.80% | 98.09% ± 0.67% |
| Logistic Regression | 98.40% | 98.39% ± 0.97% |

> El SVM ganó por criterio de test accuracy. El modelo carga con `joblib.load('model/model.pkl')`.
> Para predecir: escalar con `scaler.pkl` → predecir → decodificar con `label_encoder.pkl`

---

## Integración con Telegram
- Crear un bot con @BotFather en Telegram
- Guardar el token en `config.json` (no en el código fuente)
- El sistema envía el mensaje detectado al presionar el botón
- Se debe mostrar evidencia (capturas o video) del bot funcionando

---

## Entregables Requeridos
1. ✅ Repositorio GitHub con código completo
2. ⬜ Dataset propio organizado por clases
3. ⬜ `model.pkl` + script de entrenamiento
4. ⬜ Evidencia del bot de Telegram funcionando
5. ⬜ `Dockerfile` + `docker-compose.yml` funcionales
6. ⬜ Manual técnico (con diagramas de arquitectura)
7. ⬜ Manual de usuario

---

## División del Trabajo Sugerida (2 personas)
| Persona 1 | Persona 2 |
|---|---|
| Recolección de datos + script de captura | Entrenamiento y evaluación del modelo |
| Integración Computer Vision (MediaPipe) | Interfaz gráfica (Tkinter/PyQt5) |
| Bot de Telegram | Módulo administrativo |
| Dockerfile | README + Manuales |

---

## Estado Actual del Proyecto (10/04/2026)
- [x] Repositorio creado en GitHub
- [x] Colaboradores agregados (JosueC23, roberto1206, ixchop98)
- [x] Estructura de carpetas del proyecto
- [x] `requirements.txt` con versiones fijadas
- [x] `config.json` con configuración central
- [x] Script de recolección de dataset (`data/collect_data.py`)
- [x] Dataset recolectado — 1246 muestras, 10 clases
- [x] Script de entrenamiento (`model/train.py`) con 4 algoritmos
- [x] Modelo entrenado y guardado — SVM 100% accuracy
- [ ] **Interfaz principal `app.py`** ← SIGUIENTE PASO
- [ ] Bot de Telegram (`src/telegram_bot.py`)
- [ ] Módulo administrativo (`src/admin_panel.py`)
- [ ] Docker (`Dockerfile` + `docker-compose.yml`)
- [ ] Manuales (técnico + usuario)

## Próximo paso
Crear `app.py` — interfaz principal con Tkinter que:
1. Muestra el video en tiempo real
2. Carga `model.pkl`, `scaler.pkl`, `label_encoder.pkl`
3. Predice la seña en cada frame
4. Muestra la predicción + nivel de confianza
5. Tiene botón "Enviar a Telegram"

---

## Instrucciones para el Asistente IA
- El proyecto usa **Python como único lenguaje permitido**
- No se puede copiar código de otros grupos o de ciclos anteriores
- Si se usa código de referencia, debe referenciarse y comprenderse completamente
- Prioridad actual: construir todo antes del **1 de mayo de 2026**
- Los dos programadores trabajarán en paralelo, por lo que el código debe estar bien modularizado
- Usar `config.json` para tokens y configuración sensible (no hardcodear)
- El sistema debe funcionar dentro de Docker al final
