from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .socialmedia_addiction_input import SocialmediaAddictionInput

import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = os.path.join("models", "socialmedia-addication", "INPUT_model_path", "socialmedia_addiction_regressor_model.pkl")
model: Pipeline = joblib.load(model_path)

@app.post('/socialmedia-addiction')
async def calculateAddiction(dto: SocialmediaAddictionInput):
    input = dto.to_dict()
    
    input_df = pd.DataFrame(input)
    
    addiction_score = model.predict(input_df)[0]
    addiction_score = round(float(addiction_score), 1) 
    return {"addiction_score": addiction_score}