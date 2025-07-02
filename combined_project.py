"""
HEECCNB: An Efficient IoT-Cloud Architecture for Secure Patient Data Transmission
and Accurate Disease Prediction in Healthcare Systems

Combined Python Backend Code: Includes
1. Flask API (data receiver + ML prediction)
2. AES Encryption Utility
3. Firebase Push Integration

NOTE:
- Upload 'serviceAccountKey.json' to the same directory to use Firebase
- This script simulates how components work together
"""

# -------------------- Imports --------------------
from flask import Flask, request, jsonify
from sklearn.naive_bayes import GaussianNB
from Crypto.Cipher import AES
import base64
import numpy as np
import threading
import firebase_admin
from firebase_admin import credentials, db

# -------------------- AES Encryption Utils --------------------
key = b'ThisIsASecretKey1'      # 16 bytes
iv = b'ThisIsAnIV123456'        # 16 bytes

def encrypt(data):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return base64.b64encode(cipher.encrypt(data.encode())).decode()

def decrypt(enc_data):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(base64.b64decode(enc_data)).decode()

# -------------------- Firebase Initialization --------------------
def init_firebase():
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://heeccnb-health-care-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
        return True
    except Exception as e:
        print("Firebase not initialized:", e)
        return False

firebase_enabled = init_firebase()

def push_to_firebase(temp, bpm, status):
    if not firebase_enabled:
        return
    try:
        ref = db.reference('/health_data')
        ref.push({
            'temperature': temp,
            'bpm': bpm,
            'prediction': status
        })
        print("Data pushed to Firebase.")
    except Exception as e:
        print("Firebase push error:", e)

# -------------------- ML Model --------------------
X = np.array([[98.6, 75], [100.4, 90], [101.2, 88], [96.8, 70]])
y = np.array(['Normal', 'Fever', 'Fever', 'Normal'])
model = GaussianNB()
model.fit(X, y)

# -------------------- Flask API --------------------
app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        temp = float(request.form['temp'])
        bpm = float(request.form['bpm'])
        result = model.predict([[temp, bpm]])[0]

        print(f"Received Temp: {temp}, BPM: {bpm} -> Prediction: {result}")

        # Optional: Push to Firebase
        threading.Thread(target=push_to_firebase, args=(temp, bpm, result)).start()

        return jsonify({'status': 'success', 'prediction': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# -------------------- Start Server --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
