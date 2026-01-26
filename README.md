# AI-Based Plant Disease Detection System

## Project Overview
**Roll No:** 28, 29, 30, 32

**Problem Statement:** Develop a deep learning model to classify plant leaf diseases from images to aid in early disease detection for sustainable agriculture.

**Approach:**
This project uses **Transfer Learning** with a Convolutional Neural Network (CNN). We leverage a pre-trained model (e.g., **MobileNetV2** or **ResNet50**) trained on ImageNet and fine-tune it for plant disease classification.

**Outcomes:**
- A trained Deep Learning classifier.
- Accuracy metrics and evaluation plots.
- A demo web application for real-time inference.

**Dataset:** [Plant Disease Dataset (Kaggle)](https://www.kaggle.com/datasets/emmarex/plantdisease)

## Directory Structure
- `notebooks/`: Contains the Jupyter Notebook for training the model.
- `app/`: Contains the Streamlit demo application.
- `src/`: Source code for model definitions (optional usage).
- `models/`: Directory where trained models will be saved.

## Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook or Google Colab

### Installation (Local)
1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### 1. Training the Model
You can train the model using the provided notebook.
- **Local:** Open `notebooks/Plant_Disease_Detection.ipynb` in Jupyter/VS Code.
- **Google Colab:** Upload the notebook to Google Colab and run the cells. The notebook includes code to download the dataset directly using the Kaggle API.

#### 2. Running the Demo App
After training (or if you have a pre-trained model `plant_disease_model.h5`), run the Streamlit app:
```bash
streamlit run app/app.py
```

## Dataset Setup
The notebook uses `kagglehub` to download the dataset automatically. If running locally, ensure you have an internet connection or manually place the dataset in the `dataset/` folder.

## Technologies Used
- **TensorFlow/Keras**: For Deep Learning.
- **OpenCV/Pillow**: For image processing.
- **Streamlit**: For the web interface.
- **Matplotlib/Seaborn**: For visualization.
