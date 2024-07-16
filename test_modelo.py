import pickle

with open('face_encodings.pkl', 'rb') as f:
    known_face_encodings, known_face_names = pickle.load(f)

print(f'Codificaciones cargadas: {len(known_face_encodings)}')
print(f'Nombres cargados: {known_face_names}')