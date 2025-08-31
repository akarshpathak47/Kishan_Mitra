import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import json
from PIL import Image

# Import recommendation logic from the same folder
from recommendations import get_recommendations

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Define paths to your ML model and class names JSON
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'crop_disease_model_best_weights.h5')
CLASS_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'class_names.json')

# Load the trained model and class names
model = None
class_names = None

def load_ml_resources():
    """Loads the ML model and class names into memory."""
    global model, class_names
    try:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print(f"ML model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"Error loading ML model from {MODEL_PATH}: {e}")
        model = None

    try:
        with open(CLASS_NAMES_PATH, 'r') as f:
            class_names = json.load(f)
            print(f"Class names loaded successfully from {CLASS_NAMES_PATH}")
    except Exception as e:
        print(f"Error loading class names from {CLASS_NAMES_PATH}: {e}")
        class_names = None

# Load resources when the Flask app starts
with app.app_context():
    load_ml_resources()

@app.route('/')
def home():
    return "Kisan Mitra Backend API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or class_names is None:
        return jsonify({"error": "ML model or class names could not be loaded."}), 500

    # Check if an image file is present in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the image file directly from the stream
        img = Image.open(file.stream).convert('RGB')
        img = img.resize((224, 224))  # Resize to model's expected input shape

        # Convert image to a numpy array and normalize
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension (1, 224, 224, 3)
        img_array /= 255.0  # Normalize pixel values to [0, 1]

        # Make prediction
        predictions = model.predict(img_array)
        predicted_class_idx = np.argmax(predictions[0])  # Get the index of the highest probability
        confidence = float(np.max(predictions[0]))  # Get the confidence score

        # Map the predicted index to the actual disease name
        predicted_disease = class_names.get(str(predicted_class_idx), "Unknown Disease")

        # Get recommendations based on the predicted disease
        recommendations = get_recommendations(predicted_disease)

        return jsonify({
            "disease": predicted_disease,
            "confidence": f"{confidence * 100:.2f}%",
            "recommendations": recommendations
        })

    except Exception as e:
        app.logger.error(f"Prediction error: {e}", exc_info=True)
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # ✅ Dynamic port for Render
    app.run(debug=False, host='0.0.0.0', port=port)
