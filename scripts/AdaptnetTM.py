# AdaptnetTM.py
import os
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.exceptions import DataConversionWarning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Suppress warnings
warnings.filterwarnings('ignore', category=DataConversionWarning)

class AdaptationNetTrainer:
    def __init__(self):
        # Define paths
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.join(self.current_dir, '../data/climate_vulnerability_dataset.csv')
        self.model_dir = os.path.join(self.current_dir, '../models')
        
        # Define feature columns
        self.numerical_cols = [
            'Temperature_Anomaly', 
            'Precipitation_Change', 
            'Drought_Index', 
            'Latitude', 
            'Longitude', 
            'Elevation'
        ]
        self.categorical_cols = [
            'Climate_Risk_Level', 
            'Land_Use_Type'
        ]
        
        # Define category mappings
        self.risk_level_mapping = {
            'Very Low': 0,
            'Low': 1,
            'Medium': 2,
            'High': 3,
            'Very High': 4
        }
        
        self.land_use_mapping = {
            'Natural': 0,
            'Agricultural': 1,
            'Urban': 2,
            'Mixed': 3
        }
        
        # Ensure model directory exists
        os.makedirs(self.model_dir, exist_ok=True)
        
    def load_dataset(self):
        """Load and validate the dataset."""
        try:
            dataset = pd.read_csv(self.data_path)
            print("Dataset loaded successfully!")
            print("\nDataset preview:")
            print(dataset.head())
            print("\nColumn types:")
            print(dataset.dtypes)
            
            # Validate required columns
            required_cols = self.numerical_cols + self.categorical_cols
            missing_cols = [col for col in required_cols if col not in dataset.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
                
            return dataset
        except FileNotFoundError:
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
        except Exception as e:
            raise Exception(f"Error loading dataset: {str(e)}")

    def preprocess_data(self, dataset):
        """Preprocess the dataset for training."""
        print("\nPreprocessing data...")
        try:
            # Handle missing values in numerical columns
            dataset[self.numerical_cols] = dataset[self.numerical_cols].fillna(
                dataset[self.numerical_cols].mean()
            )
            
            # Print unique values in categorical columns
            print("\nUnique values in categorical columns:")
            for col in self.categorical_cols:
                print(f"{col}: {dataset[col].unique()}")
            
            # Create fresh copies of label encoders
            label_encoders = {}
            
            # Handle Climate Risk Level
            risk_encoder = LabelEncoder()
            if dataset['Climate_Risk_Level'].dtype == 'O':  # If text categories
                # Map text categories to numbers first
                dataset['Climate_Risk_Level'] = dataset['Climate_Risk_Level'].map(self.risk_level_mapping)
            dataset['Climate_Risk_Level'] = dataset['Climate_Risk_Level'].fillna(0)
            risk_encoder.fit([0, 1, 2, 3, 4])
            dataset['Climate_Risk_Level'] = risk_encoder.transform(dataset['Climate_Risk_Level'].astype(int))
            label_encoders['Climate_Risk_Level'] = risk_encoder
            
            # Handle Land Use Type
            land_encoder = LabelEncoder()
            if dataset['Land_Use_Type'].dtype == 'O':  # If text categories
                # Map text categories to numbers first
                dataset['Land_Use_Type'] = dataset['Land_Use_Type'].map(self.land_use_mapping)
            dataset['Land_Use_Type'] = dataset['Land_Use_Type'].fillna(0)
            land_encoder.fit([0, 1, 2, 3])
            dataset['Land_Use_Type'] = land_encoder.transform(dataset['Land_Use_Type'].astype(int))
            label_encoders['Land_Use_Type'] = land_encoder
            
            # Scale numerical features
            scaler = StandardScaler()
            feature_cols = self.numerical_cols + self.categorical_cols
            dataset[feature_cols] = scaler.fit_transform(dataset[feature_cols])
            
            # Save preprocessors
            self.save_preprocessors(label_encoders, scaler)
            
            print("Preprocessing complete!")
            return dataset, feature_cols
            
        except Exception as e:
            print("\nPreprocessing error details:")
            print(f"Dataset shape: {dataset.shape}")
            print("\nColumn info:")
            for col in self.categorical_cols:
                print(f"{col} unique values: {dataset[col].unique()}")
            raise Exception(f"Error during preprocessing: {str(e)}")

    def save_preprocessors(self, label_encoders, scaler):
        """Save preprocessing objects."""
        try:
            joblib.dump(label_encoders, os.path.join(self.model_dir, 'label_encoders.pkl'))
            joblib.dump(scaler, os.path.join(self.model_dir, 'scaler.pkl'))
            joblib.dump({
                "numerical_cols": self.numerical_cols,
                "categorical_cols": self.categorical_cols
            }, os.path.join(self.model_dir, 'feature_order.pkl'))
            print("Preprocessors saved successfully!")
        except Exception as e:
            raise Exception(f"Error saving preprocessors: {str(e)}")

    def train_kmeans(self, data, feature_cols, n_clusters=5):
        """Train KMeans clustering model."""
        print("Training KMeans model...")
        try:
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=42,
                n_init=10
            )
            kmeans.fit(data[feature_cols])
            
            # Save the model
            model_path = os.path.join(self.model_dir, 'kmeans_model.pkl')
            joblib.dump(kmeans, model_path)
            print("KMeans model trained and saved successfully!")
            
            return kmeans
        except Exception as e:
            raise Exception(f"Error during KMeans training: {str(e)}")

    def analyze_clusters(self, data, feature_cols, kmeans_model):
        """Analyze and save cluster information."""
        print("Analyzing clusters...")
        try:
            # Add cluster labels to dataset
            data['Cluster'] = kmeans_model.predict(data[feature_cols])
            
            # Calculate cluster statistics
            cluster_stats = data.groupby('Cluster')[self.numerical_cols].mean()
            
            # Save clustered data
            output_path = os.path.join(self.model_dir, 'clustered_data.csv')
            data.to_csv(output_path, index=False)
            
            # Print cluster insights
            print("\nCluster Statistics:")
            print(cluster_stats)
            print("\nSamples per cluster:", data['Cluster'].value_counts())
            
        except Exception as e:
            raise Exception(f"Error during cluster analysis: {str(e)}")

    def train(self):
        """Execute the complete training pipeline."""
        try:
            print("Starting AdaptationNet training pipeline...")
            
            # Load dataset
            dataset = self.load_dataset()
            
            # Preprocess data
            processed_data, feature_cols = self.preprocess_data(dataset)
            
            # Train KMeans model
            kmeans_model = self.train_kmeans(processed_data, feature_cols)
            
            # Analyze clusters
            self.analyze_clusters(processed_data, feature_cols, kmeans_model)
            
            print("\nTraining pipeline completed successfully!")
            
        except Exception as e:
            print(f"\nError in training pipeline: {str(e)}")
            raise

def main():
    """Main execution function."""
    try:
        trainer = AdaptationNetTrainer()
        trainer.train()
    except Exception as e:
        print(f"Training failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()