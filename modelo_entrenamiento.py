import face_recognition # Reconocimiento facial
import os # Manejo de archivos y directorios
import numpy as np # Operaciones con matrices
import pickle # Serializar y deserializar objetos
from PIL import Image # Procesamiento imágenes (conversión a RGB)

# Función para cargar las listas existentes desde el archivo
def load_known_faces(filename):
    # Verifica si el archivo de codificaciones existe
    if os.path.exists(filename):
        # Abre el archivo en modo lectura binaria
        with open(filename, "rb") as f:
            return pickle.load(f)
    # Si el archivo no existe, devuelve listas vacías
    return [], []

# Función para guardar las listas actualizadas en el archivo
def save_known_faces(filename, encodings, names):
    # Abre el archivo en modo escritura binaria
    with open(filename, "wb") as f:
        # Guarda las listas de codificaciones y nombres en el archivo
        pickle.dump((encodings, names), f)

# Directorio que contiene las nuevas imágenes
images_dir = "imagenes"
# Archivo donde se guardan las codificaciones y nombres conocidos
encodings_file = "face_encodings.pkl"

# Cargar las listas existentes
# Carga las codificaciones faciales y nombres desde el archivo existente
known_face_encodings, known_face_names = load_known_faces(encodings_file)

# Recorrer todas las nuevas imágenes en el directorio
# Recorre cada archivo en el directorio de nuevas imágenes
for image_name in os.listdir(images_dir):
    # Procesa solo los archivos con extensiones .jpg o .png
    if image_name.endswith(".jpg") or image_name.endswith(".png"):
        # Construye la ruta completa del archivo de imagen
        image_path = os.path.join(images_dir, image_name)
        
        # Carga la imagen usando PIL
        try:
            pil_image = Image.open(image_path).convert('RGB')
        except Exception as e:
            continue
        
        # Convertir la imagen a numpy array
        rgb_image = np.array(pil_image)
        
        # Verificar que la imagen tiene 3 canales de color y es uint8
        if rgb_image.dtype != np.uint8 or len(rgb_image.shape) != 3 or rgb_image.shape[2] != 3:
            continue

        # Detectar las ubicaciones de las caras
        try:
            face_locations = face_recognition.face_locations(rgb_image)
            if not face_locations:
                continue
        except Exception as e:
            continue

        # Obtener la codificación facial
        try:
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            # Verifica si se encontró al menos una codificación facial
            if face_encodings:
                # Usa la primera codificación encontrada
                face_encoding = face_encodings[0]
                # Agrega la codificación y el nombre (sin extensión) a las listas
                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(image_name)[0])
        except Exception as e:
            continue

# Guardar las listas actualizadas en el archivo
# Guarda las codificaciones faciales y nombres actualizados en el archivo
save_known_faces(encodings_file, known_face_encodings, known_face_names)

print("Todas las nuevas imágenes y nombres han sido añadidos exitosamente.")
