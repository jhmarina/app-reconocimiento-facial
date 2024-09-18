# Proyecto de Reconocimiento Facial en Tiempo Real

Este proyecto es una aplicación de reconocimiento facial en tiempo real que utiliza la biblioteca `face_recognition` y otras tecnologías de IA para detectar e identificar rostros a través de una cámara web. 
###La aplicación está diseñada para ser desplegada fácilmente en entornos como Docker y Kubernetes.

## Índice
- [Librerías utilizadas](#librerías-utilizadas)
- [Descripción de los archivos](#descripción-de-los-archivos)
- [Instrucciones para configurar el entorno](#instrucciones-para-configurar-el-entorno)
- [Cómo ejecutar la aplicación localmente](#cómo-ejecutar-la-aplicación-localmente)
- [Creación del contenedor Docker](#creación-del-contenedor-docker)
- [Despliegue en Kubernetes](#despliegue-en-kubernetes)
- [Futuras mejoras](#futuras-mejoras)

## Librerías Utilizadas

1. **`face_recognition`**: Utilizada para detectar y reconocer rostros. Esta biblioteca simplifica el reconocimiento facial utilizando modelos preentrenados.
2. **`numpy`**: Manipula las imágenes como arrays numéricos para su procesamiento.
3. **`Pillow`**: Biblioteca de procesamiento de imágenes utilizada para cargar y transformar las imágenes antes de su procesamiento.
4. **`pickle`**: Se utiliza para serializar y guardar las codificaciones faciales y los nombres en archivos.
5. **`Flask`**: Framework web en Python para crear la interfaz y API que permite procesar las imágenes en tiempo real.
6. **`gspread` y `google-auth`**: Utilizadas para conectar la aplicación a Google Sheets y registrar las detecciones de rostros.

## Descripción de los Archivos

### `app.py`
Este archivo contiene la lógica del servidor web utilizando **Flask**. La aplicación permite:
- **Capturar video en tiempo real** desde la cámara web.
- **Detectar y reconocer rostros** utilizando las codificaciones faciales generadas por el archivo de entrenamiento.
- **Registrar las detecciones** en tiempo real en una hoja de Google Sheets.
- Proveer una interfaz de usuario para visualizar el video en tiempo real y las detecciones.

### `modelo_entrenamiento.py`
Este script se encarga de:
- Procesar imágenes de rostros almacenadas en el directorio `imagenes/`.
- Extraer las **codificaciones faciales** utilizando la biblioteca `face_recognition`.
- Guardar estas codificaciones en un archivo (`codificaciones.pkl`), que luego será utilizado por la aplicación Flask para identificar rostros en tiempo real.

### `test_entrenamiento.py`
Este archivo contiene pruebas automatizadas para verificar que el modelo de entrenamiento funcione correctamente, incluyendo:
- Verificación de que se detectan los rostros en las imágenes de prueba.
- Validación de que las codificaciones se almacenan correctamente en el archivo `pickle`.

## Instrucciones para Configurar el Entorno

### 1. Crear y Activar un Entorno Virtual en Python
Para aislar las dependencias del proyecto, es recomendable utilizar un entorno virtual. Sigue los pasos a continuación:

#### En Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

## Instalar las Dependencias
Instala las dependencias necesarias desde el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

El archivo requirements.txt debe contener:

```bash
face_recognition
Flask
numpy
Pillow
gspread
google-auth
opencv-python-headless
```

## Cómo Ejecutar la Aplicación Localmente

### 1. Entrenar el Modelo
Antes de ejecutar la aplicación, necesitas procesar las imágenes y generar las codificaciones faciales. Ejecuta el script `modelo_entrenamiento.py`:

### 2. Ejecutar la Aplicación
Una vez que el modelo esté entrenado, puedes iniciar la aplicación Flask:

```bash
python app.py
```

Luego, abre un navegador y accede a `http://localhost:5000` para ver la aplicación en acción.

## Creación del Contenedor Docker

### 1. Crear el Dockerfile
Asegúrate de que tu directorio contenga un archivo `Dockerfile` con el siguiente contenido:

```bash 
# Utilizar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación al directorio de trabajo
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que correrá la aplicación Flask
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
```

### 2. Construir la Imagen de Docker
```bash
docker build -t face-recognition-app .
```

### Ejecutar el Contenedor de Docker
```bash
docker run -p 5000:5000 face-recognition-app
```
Esto ejecutará la aplicación dentro de un contenedor Docker y estará disponible en `http://localhost:5000`.

## Despliegue en Kubernetes
Para desplegar la aplicación en un clúster de Kubernetes, sigue estos pasos:

### 1.Crear el Archivo YAML de Kubernetes
Crea un archivo `kubernetes-deployment.yaml` con el siguiente contenido:


```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: face-recognition-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: face-recognition
  template:
    metadata:
      labels:
        app: face-recognition
    spec:
      containers:
      - name: face-recognition
        image: face-recognition-app:latest
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: face-recognition-service
spec:
  selector:
    app: face-recognition
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

### 2. Desplegar en el Clúster de Kubernetes
- Sube la imagen de Docker a un registro de contenedores (por ejemplo, Docker Hub o Google Container Registry).
- Edita el archivo YAML para usar la imagen subida.
- Aplica el archivo YAML en Kubernetes:

```bash
kubectl apply -f kubernetes-deployment.yaml
```

### 3. Verificar el Despliegue
Puedes verificar que el despliegue esté funcionando con los siguientes comandos:

```bash
kubectl get deployments
kubectl get services
```