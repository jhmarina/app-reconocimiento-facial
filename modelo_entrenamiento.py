import face_recognition
import os
import numpy as np
import pickle
from PIL import Image

# Función para cargar las listas existentes desde el archivo
def load_known_faces(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return [], []

# Función para guardar las listas actualizadas en el archivo
def save_known_faces(filename, encodings, names):
    with open(filename, "wb") as f:
        pickle.dump((encodings, names), f)

# Directorio que contiene las nuevas imágenes
imagenes_dir = "imagenes"
# Archivo donde se guardan las codificaciones y nombres conocidos
encodings_file = "face_encodings.pkl"

# Cargar las listas existentes
known_face_encodings, known_face_names = load_known_faces(encodings_file)

# Recorrer todas las nuevas imágenes en el directorio
for image_name in os.listdir(imagenes_dir):
    if image_name.endswith(".jpg") or image_name.endswith(".png"):
        image_path = os.path.join(imagenes_dir, image_name)
        
        try:
            pil_image = Image.open(image_path).convert('RGB')
        except Exception as e:
            continue
        
        rgb_image = np.array(pil_image)
        
        if rgb_image.dtype != np.uint8 or len(rgb_image.shape) != 3 or rgb_image.shape[2] != 3:
            continue

        rgb_image = rgb_image.astype(np.uint8)
        
        try:
            face_locations = face_recognition.face_locations(rgb_image)
            if not face_locations:
                continue
        except Exception as e:
            continue

        try:
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            if face_encodings:
                face_encoding = face_encodings[0]
                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(image_name)[0])
        except Exception as e:
            continue

save_known_faces(encodings_file, known_face_encodings, known_face_names)

print("Todas las nuevas imágenes y nombres han sido añadidos exitosamente.")
