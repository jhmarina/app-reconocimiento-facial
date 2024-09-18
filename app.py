from flask import Flask, render_template, Response, jsonify
import face_recognition
import cv2
import pickle
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Cargar el modelo de reconocimiento facial
with open("codificaciones.pkl", "rb") as f:
    known_face_encodings, known_face_names = pickle.load(f)

# Lista para almacenar las detecciones
detections = []

# Autenticación y conexión con Google Sheets
def init_google_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("credenciales.json", scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("Reconocimiento facial").sheet1
    return sheet

# Función para agregar datos a Google Sheets
def add_detection_to_sheet(sheet, name, time):
    sheet.append_row([name, time])

# Inicializar Google Sheets
sheet = init_google_sheets()

def gen_frames():
    # Abrir la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return
    
    # Reducir la resolución del video
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Ancho
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Altura
    
    while True:
        success, frame = cap.read()
        if not success:
            print("Error: No se pudo leer el frame de la cámara.")
            break
        else:
            try:
                # Convertir la imagen de BGR (OpenCV) a RGB (face_recognition)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Encontrar todas las caras y codificaciones faciales en el marco
                face_locations = face_recognition.face_locations(rgb_frame, model='hog')  # Usar HOG en lugar de CNN
                if not face_locations:
                    print("Advertencia: No se encontraron ubicaciones de rostros.")
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for face_encoding, face_location in zip(face_encodings, face_locations):
                    # Comparar las caras con las codificaciones conocidas
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    # Obtener la hora actual
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Agregar la detección a la lista
                    detections.append({"name": name, "time": current_time})

                    # Enviar la detección a Google Sheets
                    add_detection_to_sheet(sheet, name, current_time)

                    # Mostrar el nombre y la hora en la imagen
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, f"{name} {current_time}", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

                # Convertir la imagen a JPEG y devolverla
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    print("Error: No se pudo convertir el frame a JPEG.")
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print(f"Error durante el procesamiento del frame: {e}")
                break
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detections')
def get_detections():
    return jsonify(detections)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
