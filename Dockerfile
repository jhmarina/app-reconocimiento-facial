# Utilizar una imagen base de Python
FROM python:3.8-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libopenmpi-dev \
    libjpeg-dev \
    python3-dev \
    python3-pip \
    git \
    wget && \
    apt-get clean

# Crear un usuario no root
RUN useradd -ms /bin/bash appuser
USER appuser
WORKDIR /home/appuser/app

# Actualizar pip
RUN pip install --upgrade pip

# Copiar los archivos de la aplicación al contenedor
COPY --chown=appuser:appuser . .

# Instalar numpy primero
RUN pip install numpy==1.24.4

# Instalar dlib
RUN pip install dlib==19.22.1

# Instalar el resto de las dependencias de Python
RUN pip install -r requirements.txt

# Exponer el puerto de la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "modelo_entrenamiento.py"]
