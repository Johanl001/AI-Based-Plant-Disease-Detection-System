import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import json
import os

# Set page config
st.set_page_config(
    page_title="Plant Disease Detector",
    page_icon="🌿",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
    }
    .stHeader {
        color: #2E7D32;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 Plant Disease Detection System")
st.markdown("### Deep Learning based classification")

# Load Class Names
# The notebook saves class_names.json in the working directory.
# We'll check a few locations.
CLASS_NAMES_PATH = 'class_names.json'
if not os.path.exists(CLASS_NAMES_PATH):
    # Try looking in notebooks folder if running from root
    if os.path.exists('notebooks/class_names.json'):
        CLASS_NAMES_PATH = 'notebooks/class_names.json'

class_names = []
if os.path.exists(CLASS_NAMES_PATH):
    with open(CLASS_NAMES_PATH, 'r') as f:
        class_names = json.load(f)
else:
    st.warning("⚠️ 'class_names.json' not found. Please train the model first or place the file in the directory.")

# Load Model
@st.cache_resource
def load_model():
    model_paths = [
        'plant_disease_model.h5',
        'notebooks/plant_disease_model.h5',
        'models/plant_disease_model.h5'
    ]
    for path in model_paths:
        if os.path.exists(path):
            return tf.keras.models.load_model(path)
    return None

model = load_model()

if model is None:
    st.error("❌ Model file ('plant_disease_model.h5') not found. Please train the model using the notebook first.")
else:
    st.success("✅ Model loaded successfully!")

    # File Uploader
    uploaded_file = st.file_uploader("Choose a plant leaf image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width=True)
        
        if st.button("Analyze Image"):
            with st.spinner('Analyzing...'):
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
                confidence = prediction[0][index]
                
                if class_names:
                    class_name = class_names[index]
                    st.markdown(f"### Prediction: **{class_name}**")
                    st.info(f"Confidence: {confidence*100:.2f}%")
                    
                    # Simple bar chart of top 3 predictions
                    top_3_indices = np.argsort(prediction[0])[-3:][::-1]
                    top_3_values = prediction[0][top_3_indices]
                    top_3_labels = [class_names[i] for i in top_3_indices]
                    
                    st.bar_chart(data={label: val for label, val in zip(top_3_labels, top_3_values)})
                else:
                    st.write(f"Class Index: {index} (Labels missing)")

st.markdown("---")
st.markdown("Created by Roll No: 28, 29, 30, 32")
