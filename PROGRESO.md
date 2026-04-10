# HandTalk AI — Progreso del Proyecto
**Grupo 3 | Inteligencia Artificial 1 | 1S2026**
**Última actualización:** 10/04/2026

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

| Prioridad | Qué | Archivo(s) | Tiempo est. |
|---|---|---|---|
| 🔴 Alta | Interfaz principal — video en vivo + predicción en tiempo real | `app.py` | ~3h |
| 🔴 Alta | Bot de Telegram | `src/telegram_bot.py` | ~1h |
| 🟡 Media | Módulo administrativo — umbral, lista señas, toggle Telegram | `src/admin_panel.py` | ~2h |
| 🟡 Media | Docker | `Dockerfile`, `docker-compose.yml` | ~2h |
| 🟢 Baja | Manual técnico (con diagramas) | `manual_tecnico.md` | ~2h |
| 🟢 Baja | Manual de usuario | `manual_usuario.md` | ~1h |

---

## Progreso general

```
Completado  ████████░░░░░░░░░░░░  35%
Pendiente   ░░░░░░░░████████████  65%
```

**Fecha límite entrega final:** 01/05/2026 — quedan **21 días**

---

## Notas técnicas importantes

- **NO usar `mediapipe >= 0.10.10`** — arrastra `torch`/`triton` (>700 MB). Usar `mediapipe==0.10.9`
- **`cv2.imshow` NO funciona en Wayland** — toda UI debe usar **Tkinter**
- **Tkinter** no se instala con pip: `sudo apt install python3-tk`
- La webcam es `/dev/video0` (USB2.0 VGA UVC WebCam)
- Para mostrar video en Tkinter: `BGR → RGB → PIL.Image → ImageTk.PhotoImage`
- El token de Telegram va en `config.json`, **jamás** en el código fuente
