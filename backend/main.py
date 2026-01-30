from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import init_db, get_db, PredictionHistory
from model_loader import load_model_file, predict_image
from PIL import Image
import io
import os

app = FastAPI(title="Plant Disease Detector API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize
@app.on_event("startup")
def startup_event():
    init_db()
    # Path to model - Adjust if running from root or backend folder
    # We assume the app is run from the root or we use absolute paths
    # For simplicity, we look in ../model/ or ./model/
    model_path = "../model/plant_model.h5"
    if not os.path.exists(model_path):
        model_path = "model/plant_model.h5"
    
    # Absolute fallback for robustnes
    if not os.path.exists(model_path):
         print(f"WARNING: Model file not found at {model_path}")
    else:
        load_model_file(model_path)

@app.get("/")
def read_root():
    return {"message": "Plant Disease Detector API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        result = predict_image(image)
        
        # Save to DB
        db_record = PredictionHistory(
            filename=file.filename,
            prediction=result["class"],
            confidence=result["confidence"]
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return {
            "filename": file.filename,
            "prediction": result["class"],
            "confidence": result["confidence"],
            "id": db_record.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    records = db.query(PredictionHistory).order_by(PredictionHistory.timestamp.desc()).offset(skip).limit(limit).all()
    return records
