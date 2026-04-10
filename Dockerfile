# Dockerfile para HandTalk AI
# Construye una imagen Docker con todo lo necesario para ejecutar la aplicación

FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para resultados
RUN mkdir -p model/results

# Ejecutar la aplicación
CMD ["python", "app.py"]
