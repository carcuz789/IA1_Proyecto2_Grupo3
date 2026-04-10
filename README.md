# HandTalk AI — Grupo 3

Sistema inteligente de reconocimiento de señas manuales usando Computer Vision y Machine Learning.

**Universidad San Carlos de Guatemala — Inteligencia Artificial 1 — 1S2026**

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/carcuz789/IA1_Proyecto2_Grupo3.git
cd IA1_Proyecto2_Grupo3

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Edita `config.json` y coloca tu token de Telegram y chat_id:

```json
{
  "telegram": {
    "token": "TU_TOKEN_AQUI",
    "chat_id": "TU_CHAT_ID_AQUI"
  }
}
```

## Uso

### 1. Recolectar datos
```bash
python data/collect_data.py
```
- `A / D` → cambiar seña
- `ESPACIO` → capturar muestra
- `Q` → guardar y salir

### 2. Entrenar el modelo
```bash
python model/train.py
```

### 3. Ejecutar la aplicación
```bash
python app.py
```

## Docker

```bash
docker-compose up --build
```

## Arquitectura

```
IA_P2/
├── data/               # Dataset (recolección y procesamiento)
├── model/              # Entrenamiento y modelo guardado
├── src/                # Módulos del sistema
├── app.py              # Aplicación principal
└── config.json         # Configuración del sistema
```

## Integrantes — Grupo 3
- carcuz789
- JosueC23
