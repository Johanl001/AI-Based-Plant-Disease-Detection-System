# Plant Disease Detection System

## Overview
This is an end-to-end AI application for detecting plant diseases using Deep Learning. It features a FastAPI backend with SQLite integration and a modern React frontend with a premium dark-mode UI.

## Project Structure
- `backend/`: FastAPI application, database logic, and model loader.
- `frontend/`: React application (Vite) with responsive UI.
- `model/`: Trained Keras model (`plant_model.h5`) and class metadata.
- `notebooks/`: Jupyter notebooks for model training.

## Prerequisites
- Python 3.9+
- Node.js 16+

## Setup & Running

### 1. Backend
Open a terminal in the root directory:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The API will start at `http://localhost:8000`.

### 2. Frontend
Open a **new** terminal in the root directory:
```bash
cd frontend
npm install  # (If not already installed)
npm run dev
```
The UI will run at `http://localhost:5173`.

### 3. Usage
1. Open the frontend URL.
2. Upload a plant leaf image.
3. Click "Diagnose Disease".
4. View results and past history.

## Deployment (Docker)
Build and run the container:
```bash
docker build -t plant-disease-app .
docker run -p 8000:8000 plant-disease-app
```
