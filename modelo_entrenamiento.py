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
codificaciones = "codificaciones.pkl"

# Cargar las listas existentes
known_face_encodings, known_face_names = load_known_faces(codificaciones)
print(f"Codificaciones conocidas cargadas: {len(known_face_encodings)}")

# Recorrer todas las nuevas imágenes en el directorio
for image_name in os.listdir(imagenes_dir):
    if image_name.endswith(".jpg") or image_name.endswith(".png"):
        image_path = os.path.join(imagenes_dir, image_name)
        print(f"Procesando imagen: {image_path}")

        # Carga la imagen usando PIL y la convierte a RGB
        try:
            pil_image = Image.open(image_path).convert('RGB')
            print(f"Imagen {image_name} convertida a RGB")
        except Exception as e:
            print(f"Error al cargar la imagen {image_path} con PIL: {e}")
            continue
        
        # Convertir la imagen a un array de numpy
        try:
            rgb_image = np.array(pil_image)
            print(f"Imagen {image_name} convertida a array de numpy: Dimensiones {rgb_image.shape}, Dtype: {rgb_image.dtype}")
        except Exception as e:
            print(f"Error al convertir la imagen {image_name} a array de numpy: {e}")
            continue
        
        # Verificar que la imagen tiene 3 canales de color y es uint8
        if rgb_image.dtype != np.uint8:
            print(f"Advertencia: La imagen {image_name} no es de tipo uint8.")
            continue
        if len(rgb_image.shape) != 3:
            print(f"Advertencia: La imagen {image_name} no tiene 3 dimensiones.")
            continue
        if rgb_image.shape[2] != 3:
            print(f"Advertencia: La imagen {image_name} no tiene 3 canales de color.")
            continue

        # Asegurarse de que la imagen es de tipo uint8
        rgb_image = rgb_image.astype(np.uint8)
        
        # Detectar las ubicaciones de las caras en la imagen
        try:
            face_locations = face_recognition.face_locations(rgb_image)
            print(f"Ubicaciones de caras detectadas en {image_name}: {face_locations}")
            if not face_locations:
                print(f"Advertencia: No se detectaron caras en la imagen {image_name}.")
                continue
        except Exception as e:
            print(f"Error al detectar ubicaciones de caras en la imagen {image_name}: {e}")
            continue

        # Obtener la codificación facial para cada cara detectada
        try:
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            if face_encodings:
                face_encoding = face_encodings[0]  # Asume que hay una sola cara por imagen
                # Agrega la codificación y el nombre (sin extensión) a las listas conocidas
                known_face_encodings.append(face_encoding)
                known_face_names.append(os.path.splitext(image_name)[0])
                print(f"Codificación facial agregada para {image_name}")
            else:
                print(f"Advertencia: No se encontraron codificaciones faciales en la imagen {image_name}.")
        except Exception as e:
            print(f"Error al obtener codificación facial en la imagen {image_name}: {e}")
            continue

save_known_faces(codificaciones, known_face_encodings, known_face_names)
print("Todas las nuevas imágenes y nombres han sido añadidos exitosamente.")
