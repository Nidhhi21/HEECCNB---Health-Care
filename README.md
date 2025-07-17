# HEECCNB - IoT-Cloud Healthcare System

**HEECCNB: An Efficient IoT-Cloud Architecture for Secure Patient Data Transmission and Accurate Disease Prediction in Healthcare Systems**

This project integrates **IoT**, **cloud**, and **machine learning** to collect patient health data (temperature, BPM, SpO₂), securely transmit it, and predict potential diseases using a trained ML model.

---

## 🩺 Features

- 🌐 Real-time health data collection using **NodeMCU + sensors**
- 🔐 Data encrypted using **AES**
- 🧠 Disease prediction using **Naive Bayes classifier**
- ☁️ Firebase integration for remote monitoring
- 📊 Web-based UI for patient input and prediction
- ⚙️ Supports **Flask API** for ML model access

---

## ⚙️ Hardware Components

| Component       | Quantity |
|-----------------|----------|
| NodeMCU (ESP8266) | 1        |
| MAX30100 (SpO₂ + BPM) Sensor | 1 |
| DHT11 (optional - Temperature) | 1 |
| Jumper Wires    | As needed |
| Breadboard      | 1        |

---

## 🧪 Software & Libraries

- Python 3.10+
- Flask
- Firebase Admin SDK
- scikit-learn
- pycryptodome
- Arduino IDE (for NodeMCU)

### 📦 Python Installations
```bash
pip install flask firebase-admin scikit-learn pycryptodome
