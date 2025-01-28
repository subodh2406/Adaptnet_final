# model_utils.py
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATHS = {
    "scaler": os.path.join(BASE_DIR, "models", "scaler.pkl"),
    "label_encoders": os.path.join(BASE_DIR, "models", "label_encoders.pkl"),
    "feature_order": os.path.join(BASE_DIR, "models", "feature_order.pkl"),
    "kmeans": os.path.join(BASE_DIR, "models", "kmeans_model.pkl")
}

def ensure_label_encoder_classes():
    """Ensure label encoders are trained with all possible classes"""
    climate_risk_encoder = LabelEncoder()
    land_use_encoder = LabelEncoder()
    
    # Fit with all possible values
    climate_risk_encoder.fit([0, 1, 2, 3, 4])  # All possible climate risk levels
    land_use_encoder.fit([0, 1, 2, 3])  # All possible land use types
    
    return {
        "Climate_Risk_Level": climate_risk_encoder,
        "Land_Use_Type": land_use_encoder
    }

def load_all_models():
    """Load all required models and preprocessors."""
    models = {}
    try:
        # Load the models
        for key, path in MODEL_PATHS.items():
            if not os.path.exists(path):
                raise FileNotFoundError(f"Model file not found: {path}")
            models[key] = joblib.load(path)
        
        # Ensure label encoders are properly initialized
        models["label_encoders"] = ensure_label_encoder_classes()
        
        return models
    except Exception as e:
        raise Exception(f"Error loading models: {str(e)}")

def preprocess_input(features, models):
    """Preprocess input features using loaded models."""
    try:
        df = pd.DataFrame([features])
        
        # Get feature order
        feature_order = models["feature_order"]
        numerical_cols = feature_order["numerical_cols"]
        categorical_cols = feature_order["categorical_cols"]
        
        # Convert categorical values to integers if they're not already
        for col in categorical_cols:
            df[col] = df[col].astype(int)
        
        # Encode categorical features
        for col in categorical_cols:
            df[col] = models["label_encoders"][col].transform(df[col])
        
        # Scale all features
        columns_to_scale = numerical_cols + categorical_cols
        df[columns_to_scale] = models["scaler"].transform(df[columns_to_scale])
        
        return df[columns_to_scale]
    
    except Exception as e:
        raise Exception(f"Error preprocessing input: {str(e)}")