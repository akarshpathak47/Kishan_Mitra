import os
import json
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.preprocessing import image
from PIL import Image

# Import recommendation logic
from recommendations import get_recommendations

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
# Adjust this path if your 'ml' folder is in a different spot
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'crop_disease_model_best_weights.h5')
CLASS_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'class_names.json')

model = None
class_names = None

def load_ml_resources():
    global model, class_names
    try:
        # 1. Load Model
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            print(f"✅ SUCCESS: Model loaded from {MODEL_PATH}")
        else:
            print(f"❌ ERROR: Model file not found at {MODEL_PATH}")

        # 2. Load Class Names
        if os.path.exists(CLASS_NAMES_PATH):
            with open(CLASS_NAMES_PATH, 'r') as f:
                class_names = json.load(f)
            print(f"✅ SUCCESS: {len(class_names)} classes loaded.")
        else:
            print(f"❌ ERROR: class_names.json not found at {CLASS_NAMES_PATH}")

    except Exception as e:
        print(f"🚨 CRITICAL ERROR during loading: {e}")

# Load resources immediately
load_ml_resources()

@app.route('/')
def home():
    return "Kisan Mitra Backend API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or class_names is None:
        return jsonify({"error": "Model or class names not loaded on server."}), 500

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    try:
        # --- IMAGE PREPROCESSING ---
        img = Image.open(file.stream).convert('RGB')
        img = img.resize((224, 224)) 
        
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) 
        
        # FIX: Ensure normalization matches your training (usually 1/255)
        img_array = img_array / 255.0 

        # --- PREDICTION ---
        predictions = model.predict(img_array)
        predicted_class_idx = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))

        # --- DEBUGGING LOGS (Check your VS Code Terminal!) ---
        print("-" * 30)
        print(f"DEBUG: Predicted Index -> {predicted_class_idx}")
        print(f"DEBUG: Confidence -> {confidence:.2%}")
        
        # --- MAPPING INDEX TO NAME ---
        # Handles if class_names.json is a LIST or a DICT
        if isinstance(class_names, list):
            predicted_disease = class_names[predicted_class_idx]
        else:
            # If it's a dict like {"0": "Healthy"}, use .get()
            predicted_disease = class_names.get(str(predicted_class_idx), "Unknown Disease")

        print(f"DEBUG: Final Disease Name -> {predicted_disease}")
        print("-" * 30)

        # --- GET RECOMMENDATIONS ---
        recommendations = get_recommendations(predicted_disease)

        return jsonify({
            "disease": predicted_disease,
            "confidence": f"{confidence * 100:.2f}%",
            "recommendations": recommendations
        })

    except Exception as e:
        print(f"🚨 PREDICTION ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)