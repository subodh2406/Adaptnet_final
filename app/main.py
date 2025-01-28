# # main.py (FastAPI)
# from typing import Dict

# from fastapi import FastAPI, HTTPException
# from model_utils import load_all_models, preprocess_input
# from pydantic import BaseModel, Field

# app = FastAPI(
#     title="AdaptNet Climate Adaptation API",
#     description="API for climate adaptation recommendations using machine learning",
#     version="1.0.0"
# )

# # Load models
# try:
#     models = load_all_models()
# except Exception as e:
#     print(f"Error loading models: {str(e)}")
#     models = None

# class InputData(BaseModel):
#     features: Dict[str, float] = Field(
#         ...,
#         example={
#             "Temperature_Anomaly": 0.0,
#             "Precipitation_Change": 0.0,
#             "Drought_Index": 0.0,
#             "Latitude": 0.0,
#             "Longitude": 0.0,
#             "Elevation": 0.0,
#             "Climate_Risk_Level": 2,
#             "Land_Use_Type": 1
#         }
#     )

# class PredictionResponse(BaseModel):
#     cluster: int
#     recommendations: list[str]
#     confidence: float

# @app.get("/")
# async def root():
#     return {
#         "status": "active",
#         "model_status": "loaded" if models is not None else "not loaded",
#         "version": "1.0.0"
#     }

# @app.post("/predict")
# async def predict(data: InputData):
#     if models is None:
#         raise HTTPException(status_code=500, detail="Models not loaded")
    
#     try:
#         # Preprocess input
#         processed_input = preprocess_input(data.features, models)
        
#         # Make prediction
#         cluster = int(models["kmeans"].predict(processed_input)[0])
        
#         # Get recommendations based on cluster
#         recommendations = get_recommendations(cluster, data.features)
        
#         return {
#             "prediction": {
#                 "cluster": cluster,
#                 "recommendations": recommendations,
#                 "confidence": 0.85  # Example confidence score
#             }
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# def get_recommendations(cluster: int, features: Dict[str, float]) -> list[str]:
#     """Generate recommendations based on cluster and input features."""
#     # Add your recommendation logic here
#     base_recommendations = {
#         0: ["Low vulnerability - Focus on monitoring and maintenance"],
#         1: ["Moderate vulnerability - Implement basic adaptation measures"],
#         2: ["High vulnerability - Comprehensive adaptation strategy needed"],
#         3: ["Very high vulnerability - Urgent intervention required"],
#         4: ["Extreme vulnerability - Immediate action and support needed"]
#     }
    
#     return base_recommendations.get(cluster, ["No specific recommendations available"])




from typing import Dict
import os

from fastapi import FastAPI, HTTPException
from model_utils import load_all_models, preprocess_input
from pydantic import BaseModel, Field

app = FastAPI(
    title="AdaptNet Climate Adaptation API",
    description="API for climate adaptation recommendations using machine learning",
    version="1.0.0"
)

# Load models
try:
    models = load_all_models()
except Exception as e:
    print(f"Error loading models: {str(e)}")
    models = None

class InputData(BaseModel):
    features: Dict[str, float] = Field(
        ...,
        example={
            "Temperature_Anomaly": 0.0,
            "Precipitation_Change": 0.0,
            "Drought_Index": 0.0,
            "Latitude": 0.0,
            "Longitude": 0.0,
            "Elevation": 0.0,
            "Climate_Risk_Level": 2,
            "Land_Use_Type": 1
        }
    )

class PredictionResponse(BaseModel):
    cluster: int
    recommendations: list[str]
    confidence: float

@app.get("/")
async def root():
    return {
        "status": "active",
        "model_status": "loaded" if models is not None else "not loaded",
        "version": "1.0.0"
    }

@app.post("/predict")
async def predict(data: InputData):
    if models is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    try:
        # Preprocess input
        processed_input = preprocess_input(data.features, models)
        
        # Make prediction
        cluster = int(models["kmeans"].predict(processed_input)[0])
        
        # Get recommendations based on cluster
        recommendations = get_recommendations(cluster, data.features)
        
        return {
            "prediction": {
                "cluster": cluster,
                "recommendations": recommendations,
                "confidence": 0.85  # Example confidence score
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_recommendations(cluster: int, features: Dict[str, float]) -> list[str]:
    """Generate recommendations based on cluster and input features."""
    base_recommendations = {
        0: ["Low vulnerability - Focus on monitoring and maintenance"],
        1: ["Moderate vulnerability - Implement basic adaptation measures"],
        2: ["High vulnerability - Comprehensive adaptation strategy needed"],
        3: ["Very high vulnerability - Urgent intervention required"],
        4: ["Extreme vulnerability - Immediate action and support needed"]
    }
    
    return base_recommendations.get(cluster, ["No specific recommendations available"])

# Run the FastAPI app on the appropriate host and port for public access
if __name__ == "__main__":
    import uvicorn
    port = os.environ.get("PORT", 8000)  # Default to 8000 if PORT not set
    uvicorn.run(app, host="0.0.0.0", port=int(port))
