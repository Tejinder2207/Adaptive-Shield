from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from pathlib import Path

app = FastAPI(
    title="Adaptive Shield API",
    description="SMS Spam Classification API powered by Scikit-Learn & FastAPI",
    version="1.0.0"
)

# Define the input data model using Pydantic
class MessageRequest(BaseModel):
    text: str

# Load your trained model pipeline (adjust path if needed based on where your model is saved)
MODEL_PATH = Path("models/spam_classifier.pkl") # or your trained model artifact path

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to the Adaptive Shield SMS Spam Classifier API!"}

@app.post("/predict")
def predict_spam(payload: MessageRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty.")
    
    try:
        # Load model dynamically or ensure it's loaded at startup
        # If using your pipeline artifacts:
        # model = joblib.load(MODEL_PATH)
        # prediction = model.predict([payload.text])[0]
        
        # Placeholder response until model artifact path is finalized:
        is_spam = "free" in payload.text.lower() or "win" in payload.text.lower()
        prediction = "spam" if is_spam else "ham"
        confidence = 0.95 if is_spam else 0.88

        return {
            "text": payload.text,
            "prediction": prediction,
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))