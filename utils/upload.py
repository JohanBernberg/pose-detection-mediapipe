import firebase_admin
from firebase_admin import credentials, storage
import random 
from datetime import datetime
import cv2
import os
import json
from dotenv import load_dotenv
load_dotenv()

json_credencial = os.getenv('JSON')
credenciales = json.loads(json_credencial)

if not firebase_admin._apps:
    cred = credentials.Certificate(json_credencial)
    firebase_admin.initialize_app(cred, {'storageBucket':'load-images-5b386.appspot.com'})
bucket = storage.bucket()

def upload_firebase(img):
    imagen_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convertir la imagen a un objeto de bytes
    _, buffer = cv2.imencode('.png', imagen_rgb)
    image_bytes = buffer.tobytes()
    # Subir la imagen directamente a Firebase Storage
    bucket = storage.bucket()

    date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    id = str(random.randint(1, 100000000))
    blob = bucket.blob(f'images/{date}_{id}.png')
    blob.upload_from_string(image_bytes, content_type='image/png')