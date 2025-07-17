# -------------------- Imports --------------------
from flask import Flask, request, jsonify
from flask_cors import CORS
from Crypto.Cipher import AES
import base64
import numpy as np
import threading
import firebase_admin
from firebase_admin import credentials, db
import joblib

# -------------------- AES Encryption Utils --------------------
key = b'ThisIsASecretKey1'  # 16 bytes
iv = b'ThisIsAnIV123456'    # 16 bytes

def encrypt(data):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return base64.b64encode(cipher.encrypt(data.encode())).decode()

def decrypt(enc_data):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(base64.b64decode(enc_data)).decode()

# -------------------- Firebase Initialization --------------------
def init_firebase():
    try:
        cred = credentials.Certificate("place your key in json format ")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'place your cloud url'
        })
        return True
    except Exception as e:
        print("Firebase not initialized:", e)
        return False

firebase_enabled = init_firebase()

def push_to_firebase(temp, bpm, spo2, status):
    if not firebase_enabled:
        return
    try:
        ref = db.reference('/health_data')
        ref.push({
            'temperature': temp,
            'bpm': bpm,
            'spo2': spo2,
            'prediction': status
        })
        print("Data pushed to Firebase.")
    except Exception as e:
        print("Firebase push error:", e)

# -------------------- Load Trained Model and Label Encoder --------------------
try:
    model = joblib.load("disease_model.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    print("Model and label encoder loaded successfully.")
except Exception as e:
    print("Model loading error:", e)
    model = None
    label_encoder = None

# -------------------- Flask App --------------------
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Disease Prediction API is running!"

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        temp = float(request.form['temp'])
        bpm = float(request.form['bpm'])
        spo2 = float(request.form['spo2'])

        if model is None or label_encoder is None:
            return jsonify({'status': 'error', 'message': 'Model not loaded'})

        input_data = np.array([[temp, bpm, spo2]])
        prediction = model.predict(input_data)[0]
        result = label_encoder.inverse_transform([prediction])[0]

        print(f"Input: Temp={temp}, BPM={bpm}, SpO2={spo2} → Prediction: {result}")

        # Push to Firebase in background
        threading.Thread(target=push_to_firebase, args=(temp, bpm, spo2, result)).start()

        return jsonify({'status': 'success', 'prediction': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# -------------------- Run the Server --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
