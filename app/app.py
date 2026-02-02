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
# The notebook saves class_names.json in the working directory or model directory.
# We'll check a few locations.
CLASS_NAMES_PATH = 'class_names.json'
possible_class_paths = [
    'model/class_names.json', 
    '../model/class_names.json', 
    'class_names.json',
    'notebooks/class_names.json'
]

for path in possible_class_paths:
    if os.path.exists(path):
        CLASS_NAMES_PATH = path
        break

class_names = []
if os.path.exists(CLASS_NAMES_PATH):
    with open(CLASS_NAMES_PATH, 'r') as f:
        class_names = json.load(f)
else:
    st.warning(f"⚠️ 'class_names.json' not found. Checked: {possible_class_paths}")

# Load Model
@st.cache_resource
def load_model():
    model_paths = [
        'model/plant_model.h5',
        '../model/plant_model.h5',
        'plant_model.h5',
        'plant_disease_model.h5',
    ]
    for path in model_paths:
        if os.path.exists(path):
            return tf.keras.models.load_model(path)
    return None

model = load_model()

if model is None:
    st.error("❌ Model file ('plant_model.h5') not found. Please train the model using the notebook first.")
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
                    confidence_score = prediction[0][index]

                    # Load Disease Info
                    try:
                        with open('app/disease_info.json', 'r') as f:
                            disease_info = json.load(f)
                    except FileNotFoundError:
                        try:
                            with open('disease_info.json', 'r') as f:
                                disease_info = json.load(f)
                        except:
                            disease_info = {}

                    # Get details
                    info = disease_info.get(class_name, {
                        "name": class_name,
                        "description": "No description available.",
                        "prevention": []
                    })

                    st.markdown(f"### Diagnosis: **{info['name']}**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Confidence Score", f"{confidence_score*100:.2f}%")
                    
                    with col2:
                        st.info(f"**Description:** {info['description']}")

                    if info.get('prevention'):
                        st.subheader("🛡️ Prevention Measures")
                        for measure in info['prevention']:
                            st.write(f"- {measure}")

                    # Chart
                    st.markdown("#### Top 3 Predictions")
                    top_3_indices = np.argsort(prediction[0])[-3:][::-1]
                    top_3_values = prediction[0][top_3_indices]
                    top_3_labels = [class_names[i] for i in top_3_indices]
                    
                    chart_data = {label: val for label, val in zip(top_3_labels, top_3_values)}
                    st.bar_chart(chart_data)

                else:
                    st.write(f"Class Index: {index} (Labels missing)")

st.markdown("---")
st.markdown("Created by Roll No: 28, 29, 30, 32")
