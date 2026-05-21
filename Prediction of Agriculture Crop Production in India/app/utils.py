import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'crop_production.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

class PredictionUtils:
    """
    Utility class for crop production prediction.
    Handles model loading, data preprocessing for prediction, and utility functions.
    """

    def __init__(self, model_path=os.path.join(MODELS_DIR, 'crop_model.pkl'), scaler_path=os.path.join(MODELS_DIR, 'scaler.pkl')):
        """
        Initialize the prediction utilities.

        Args:
            model_path (str): Path to the trained model
            scaler_path (str): Path to the scaler object
        """
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        self.load_model(model_path)
        self.load_scaler(scaler_path)
        self.load_label_encoders()

    def load_model(self, model_path):
        """
        Load the trained model.

        Args:
            model_path (str): Path to the model file
        """
        try:
            self.model = joblib.load(model_path)
            print("Model loaded successfully")
        except FileNotFoundError:
            print(f"Error: Model file {model_path} not found.")
            self.model = None

    def load_scaler(self, scaler_path):
        """
        Load the scaler object.

        Args:
            scaler_path (str): Path to the scaler file
        """
        try:
            self.scaler = joblib.load(scaler_path)
            print("Scaler loaded successfully")
        except FileNotFoundError:
            print(f"Error: Scaler file {scaler_path} not found.")
            self.scaler = None

    def load_label_encoders(self):
        """
        Load all label encoders for categorical features.
        """
        encoder_files = ['state_name_encoder.pkl', 'district_name_encoder.pkl',
                        'season_encoder.pkl', 'crop_encoder.pkl']
        encoder_names = ['State_Name', 'District_Name', 'Season', 'Crop']

        for file_name, name in zip(encoder_files, encoder_names):
            try:
                encoder_path = os.path.join(MODELS_DIR, file_name)
                self.label_encoders[name] = joblib.load(encoder_path)
                print(f"{name} encoder loaded successfully")
            except FileNotFoundError:
                print(f"Warning: {name} encoder file not found. Using default encoding.")
                self.label_encoders[name] = LabelEncoder()
                self.label_encoders[name].fit(['Unknown'])  # Fit with a default value

    def preprocess_input(self, input_data):
        """
        Preprocess input data for prediction.

        Args:
            input_data (dict): Dictionary containing input features

        Returns:
            np.array: Preprocessed feature array
        """
        try:
            # Extract features
            features = {
                'Crop_Year': input_data['Crop_Year'],
                'Area': input_data['Area'],
                'Annual_Rainfall': input_data['Annual_Rainfall'],
                'Fertilizer': input_data['Fertilizer'],
                'Pesticide': input_data['Pesticide'],
                'Temperature': input_data['Temperature']
            }

            # Encode categorical features
            categorical_features = {}
            for cat_feature in ['State_Name', 'District_Name', 'Season', 'Crop']:
                if cat_feature in input_data:
                    encoder = self.label_encoders.get(cat_feature)
                    if encoder:
                        try:
                            encoded_value = encoder.transform([input_data[cat_feature]])[0]
                        except ValueError:
                            # If value not in training data, use the first class
                            encoded_value = 0
                        categorical_features[cat_feature + '_encoded'] = encoded_value

            # Combine all features
            all_features = list(features.values()) + list(categorical_features.values())

            # Scale numerical features
            if self.scaler:
                numerical_values = list(features.values())
                scaled_numerical = self.scaler.transform([numerical_values])[0]
                all_features[:6] = scaled_numerical

            return np.array([all_features])

        except Exception as e:
            print(f"Error preprocessing input: {e}")
            return None

    def predict_production(self, input_data):
        """
        Predict crop production based on input data.

        Args:
            input_data (dict): Dictionary containing input features

        Returns:
            float: Predicted production value
        """
        if self.model is None:
            print("Error: Model not loaded")
            return None

        processed_data = self.preprocess_input(input_data)
        if processed_data is not None:
            prediction = self.model.predict(processed_data)[0]
            return max(0, prediction)  # Ensure non-negative prediction
        else:
            return None

    def get_unique_values(self, column_name):
        """
        Get unique values for a categorical column from the dataset.

        Args:
            column_name (str): Name of the column

        Returns:
            list: List of unique values
        """
        try:
            # Load dataset to get unique values
            df = pd.read_csv(DATASET_PATH)
            if column_name in df.columns:
                return sorted(df[column_name].unique().tolist())
            else:
                return []
        except FileNotFoundError:
            print("Warning: Dataset not found. Using default values.")
            # Return some default values based on column
            defaults = {
                'State_Name': ['Maharashtra', 'Karnataka', 'Punjab', 'Uttar Pradesh', 'Gujarat'],
                'Season': ['Kharif', 'Rabi', 'Whole Year'],
                'Crop': ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane']
            }
            return defaults.get(column_name, [])

def load_dataset_preview():
    """
    Load a preview of the dataset for display in the app.

    Returns:
        pd.DataFrame: Preview of the dataset
    """
    try:
        df = pd.read_csv(DATASET_PATH)
        return df.head(10)
    except FileNotFoundError:
        return pd.DataFrame()

def get_dataset_info():
    """
    Get basic information about the dataset.

    Returns:
        dict: Dictionary containing dataset information
    """
    try:
        df = pd.read_csv(DATASET_PATH)
        return {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict()
        }
    except FileNotFoundError:
        return {}

# Global instance for use in the app
prediction_utils = PredictionUtils()

def get_unique_values(column_name):
    """
    Get unique values for a categorical column through the prediction utility.

    Args:
        column_name (str): Name of the dataset column to read.

    Returns:
        list: Unique values in the requested column.
    """
    return prediction_utils.get_unique_values(column_name)
