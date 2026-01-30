import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import os

model = None
class_names = []

def load_model_file(model_path: str):
    global model, class_names
    try:
        model = tf.keras.models.load_model(model_path)
        print(f"Model loaded from {model_path}")
        
        # Load class names if they exist, otherwise use placeholders or try to derive
        # Assuming a class_names.json exists or we hardcode common ones for this dataset
        # For now, we'll try to load from a json file in the same dir as model or root
        class_names_path = os.path.join(os.path.dirname(model_path), 'class_names.json')
        if not os.path.exists(class_names_path):
             class_names_path = 'class_names.json' 

        if os.path.exists(class_names_path):
            import json
            with open(class_names_path, 'r') as f:
                class_names = json.load(f)
        else:
            # Fallback or empty - User needs to ensure this
             print("Warning: class_names.json not found. Predictions will be indices.")
             
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e

def predict_image(image: Image.Image):
    global model
    if model is None:
        raise ValueError("Model not loaded")

    # Preprocess
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.LANCZOS)
    img_array = np.asarray(image)
    normalized_image_array = (img_array.astype(np.float32) / 255.0)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Predict
    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence = float(prediction[0][index])
    
    label = str(index)
    if class_names and index < len(class_names):
        label = class_names[index]
        
    return {
        "class": label,
        "confidence": confidence,
        "all_predictions": prediction[0].tolist()
    }
