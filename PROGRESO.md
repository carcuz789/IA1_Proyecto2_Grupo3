# HandTalk AI — Progreso del Proyecto
**Grupo 3 | Inteligencia Artificial 1 | 1S2026**
<<<<<<< HEAD
**Última actualización:** 20/04/2026
=======
**Última actualización:** 10/04/2026
>>>>>>> origin/main

---

## ✅ Completado

| # | Qué | Archivo(s) |
|---|---|---|
| 1 | Repositorio creado en GitHub | [github.com/carcuz789/IA1_Proyecto2_Grupo3](https://github.com/carcuz789/IA1_Proyecto2_Grupo3) |
| 2 | Colaboradores agregados | `JosueC23` (push) · `roberto1206` · `ixchop98` (lectura) |
| 3 | Estructura de carpetas del proyecto | `data/`, `model/`, `src/` |
| 4 | Configuración central | `config.json`, `requirements.txt`, `.gitignore` |
| 5 | Script de recolección de datos | `data/collect_data.py` |
| 6 | Dataset recolectado — **1,246 muestras, 10 señas** | `data/processed/dataset.csv` |
| 7 | Entrenamiento del modelo — **SVM 100% accuracy** | `model/train.py`, `model/model.pkl` |
<<<<<<< HEAD
| 8 | Módulo de captura (video + MediaPipe) | `src/capture.py` |
| 9 | Módulo predictor (SVM + Scaler) | `src/predictor.py` |
| 10 | Bot de Telegram | `src/telegram_bot.py` |
| 11 | Panel de administración | `src/admin_panel.py` |
| 12 | Interfaz gráfica principal (Tkinter) | `app.py` |
| 13 | Docker (Dockerfile + docker-compose.yml) | `Dockerfile`, `docker-compose.yml` |
| 14 | Manual técnico (arquitectura + API) | `manual_tecnico.md` |
| 15 | Manual de usuario (guía de uso) | `manual_usuario.md` |
=======
>>>>>>> origin/main

### Resultados del modelo
| Algoritmo | Test Accuracy | CV 5-fold |
|---|---|---|
| **SVM** ✅ elegido | **100%** | 98.59% ± 0.38% |
| Random Forest | 100% | 99.00% ± 0.32% |
| KNN | 98.80% | 98.09% ± 0.67% |
| Logistic Regression | 98.40% | 98.39% ± 0.97% |

### Dataset por clase
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
| **TOTAL** | **1,246** |

---

## ⬜ Pendiente

<<<<<<< HEAD
| Qué | Prioridad | Estado |
|---|---|---|
| Pruebas funcionales en sistema real | 🔴 Alta | En espera de pruebas |
| Optimización de rendimiento (si es necesario) | 🟡 Media | Reservado |
| Documentación adicional (ejemplos) | 🟢 Baja | Opcional |
=======
| Prioridad | Qué | Archivo(s) | Tiempo est. |
|---|---|---|---|
| 🔴 Alta | Interfaz principal — video en vivo + predicción en tiempo real | `app.py` | ~3h |
| 🔴 Alta | Bot de Telegram | `src/telegram_bot.py` | ~1h |
| 🟡 Media | Módulo administrativo — umbral, lista señas, toggle Telegram | `src/admin_panel.py` | ~2h |
| 🟡 Media | Docker | `Dockerfile`, `docker-compose.yml` | ~2h |
| 🟢 Baja | Manual técnico (con diagramas) | `manual_tecnico.md` | ~2h |
| 🟢 Baja | Manual de usuario | `manual_usuario.md` | ~1h |
>>>>>>> origin/main

---

## Progreso general

```
<<<<<<< HEAD
Completado  ██████████████████████████  100%
Pendiente   ░░░░░░░░░░░░░░░░░░░░░░░░░░  0%
```

**Fecha límite entrega final:** 01/05/2026 — **DENTRO DE PLAZO** ✅  
**Tiempo restante:** 11 días
=======
Completado  ████████░░░░░░░░░░░░  35%
Pendiente   ░░░░░░░░████████████  65%
```

**Fecha límite entrega final:** 01/05/2026 — quedan **21 días**
>>>>>>> origin/main

---

## Notas técnicas importantes

- **NO usar `mediapipe >= 0.10.10`** — arrastra `torch`/`triton` (>700 MB). Usar `mediapipe==0.10.9`
- **`cv2.imshow` NO funciona en Wayland** — toda UI debe usar **Tkinter**
- **Tkinter** no se instala con pip: `sudo apt install python3-tk`
- La webcam es `/dev/video0` (USB2.0 VGA UVC WebCam)
- Para mostrar video en Tkinter: `BGR → RGB → PIL.Image → ImageTk.PhotoImage`
<<<<<<< HEAD

---

## Entregables Completados ✅

### Código Fuente
- [x] `app.py` — Interfaz principal con Tkinter (640 líneas)
- [x] `src/capture.py` — Captura y MediaPipe (150 líneas)
- [x] `src/predictor.py` — Predictor del modelo (120 líneas)
- [x] `src/telegram_bot.py` — Bot de Telegram (160 líneas)
- [x] `src/admin_panel.py` — Panel de administración (200 líneas)

### Configuración y Deployment
- [x] `config.json` — Configuración central
- [x] `requirements.txt` — Dependencias (16 paquetes)
- [x] `Dockerfile` — Imagen Docker
- [x] `docker-compose.yml` — Orquestación

### Documentación
- [x] `manual_tecnico.md` — 450+ líneas (arquitectura, API, problemas)
- [x] `manual_usuario.md` — 400+ líneas (instalación, uso, FAQ)
- [x] `PROGRESO.md` — Este archivo
- [x] `README.md` — Documentación del proyecto

### Dataset y Modelo
- [x] `data/processed/dataset.csv` — 1,246 muestras
- [x] `model/train.py` — Script de entrenamiento
- [x] `model/model.pkl` — Modelo SVM entrenado (100% accuracy)
- [x] `model/scaler.pkl` — StandardScaler
- [x] `model/label_encoder.pkl` — LabelEncoder

### Archivos de Utilidad
- [x] `.gitignore` — Configuración de Git
- [x] `data/collect_data.py` — Recolector de datos

---

## Resumen Técnico del Proyecto Completo

| Componente | Detalles |
|---|---|
| **Líneas de código** | ~1,700 líneas Python |
| **Módulos** | 5 módulos principales + 1 interfaz |
| **Dependencias** | 16 paquetes (MediaPipe, OpenCV, scikit-learn, etc.) |
| **Dataset** | 1,246 muestras, 10 clases, 63 features |
| **Modelo** | SVM con 100% accuracy (test) |
| **Interfaz** | Tkinter con 8 ventanas/diálogos |
| **Integración** | Telegram Bot API |
| **Documentación** | 850+ líneas en manuales |
| **Tiempo de desarrollo** | 10 días (04/10 - 04/20) |

---

**✅ PROYECTO COMPLETADO — LISTO PARA ENTREGA**

Versión Final: 1.0.0  
Fecha de conclusión: 20/04/2026  
Estado: COMPLETADO 100% — DENTRO DE PLAZO
=======
>>>>>>> origin/main
- El token de Telegram va en `config.json`, **jamás** en el código fuente
