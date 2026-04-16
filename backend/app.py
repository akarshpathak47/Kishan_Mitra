import os
import json
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.preprocessing import image
from PIL import Image
import random

# Import recommendation logic
from recommendations import get_recommendations

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, '..', 'ml', 'crop_disease_model_best_weights.h5')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'class_name.json')  # ✅ your file name

model = None
class_names = None

def load_ml_resources():
    global model, class_names
    try:
        # --- Load Model ---
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            print(f"✅ Model loaded from {MODEL_PATH}")
        else:
            print(f"⚠️ Model not found (Demo mode active)")

        # --- Load Class Names ---
        if os.path.exists(CLASS_NAMES_PATH):
            with open(CLASS_NAMES_PATH, 'r') as f:
                class_names = json.load(f)
            print(f"✅ {len(class_names)} classes loaded")
        else:
            print(f"❌ class_name.json not found")

    except Exception as e:
        print(f"🚨 Error loading resources: {e}")

# Load resources at startup
load_ml_resources()

@app.route('/')
def home():
    return "Kisan Mitra Backend API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if class_names is None:
        return jsonify({"error": "Class names not loaded"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    try:
        # --- Image preprocessing ---
        img = Image.open(file.stream).convert('RGB')
        img = img.resize((224, 224))

        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        # --- Prediction ---
        if model is not None:
            predictions = model.predict(img_array)
            predicted_class_idx = int(np.argmax(predictions[0]))
            confidence = float(np.max(predictions[0]))
            mode = "Real prediction"
        else:
            predicted_class_idx = random.randint(0, len(class_names) - 1)
            confidence = random.uniform(0.80, 0.98)
            mode = "Demo mode"

        # --- Map class ---
        if isinstance(class_names, list):
            predicted_disease = class_names[predicted_class_idx]
        else:
            predicted_disease = class_names.get(str(predicted_class_idx), "Unknown Disease")

        print(f"Prediction: {predicted_disease} ({confidence*100:.2f}%) [{mode}]")

        # --- Recommendations ---
        recommendations = get_recommendations(predicted_disease)

        return jsonify({
            "disease": predicted_disease,
            "confidence": f"{confidence*100:.2f}%",
            "recommendations": recommendations,
            "mode": mode
        })

    except Exception as e:
        print(f"🚨 Prediction error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
