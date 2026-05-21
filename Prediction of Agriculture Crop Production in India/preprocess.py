import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

class DataPreprocessor:
    """
    Class for preprocessing crop production data.
    Handles loading, cleaning, encoding, and scaling of data.
    """

    def __init__(self, data_path='./dataset/crop_production.csv'):
        """
        Initialize the preprocessor.

        Args:
            data_path (str): Path to the dataset CSV file
        """
        self.data_path = data_path
        self.df = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.features = None
        self.target = 'Production'

    def load_data(self):
        """
        Load the dataset from CSV file.

        Returns:
            pd.DataFrame: Loaded dataframe
        """
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"Data loaded successfully. Shape: {self.df.shape}")
            return self.df
        except FileNotFoundError:
            print(f"Error: File {self.data_path} not found.")
            return None

    def clean_data(self):
        """
        Clean the data by handling missing values.

        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        # Drop rows with missing values for simplicity
        # In production, you might want to impute missing values
        initial_shape = self.df.shape
        self.df = self.df.dropna()
        final_shape = self.df.shape
        print(f"Data cleaned. Removed {initial_shape[0] - final_shape[0]} rows with missing values.")
        return self.df

    def encode_categorical_features(self):
        """
        Encode categorical features using Label Encoding.

        Returns:
            pd.DataFrame: Dataframe with encoded features
        """
        categorical_cols = ['State_Name', 'District_Name', 'Season', 'Crop']

        for col in categorical_cols:
            if col in self.df.columns:
                le = LabelEncoder()
                self.df[col + '_encoded'] = le.fit_transform(self.df[col])
                self.label_encoders[col] = le
                print(f"Encoded {col} with {len(le.classes_)} unique values")

        return self.df

    def scale_numerical_features(self):
        """
        Scale numerical features using StandardScaler.

        Returns:
            pd.DataFrame: Dataframe with scaled features
        """
        numerical_cols = ['Crop_Year', 'Area', 'Annual_Rainfall', 'Fertilizer', 'Pesticide', 'Temperature']

        # Fit and transform the scaler
        self.df[numerical_cols] = self.scaler.fit_transform(self.df[numerical_cols])
        print("Numerical features scaled using StandardScaler")
        return self.df

    def prepare_features(self):
        """
        Prepare the feature matrix and target vector.

        Returns:
            tuple: (X, y) where X is features and y is target
        """
        encoded_cols = [col + '_encoded' for col in ['State_Name', 'District_Name', 'Season', 'Crop'] if col + '_encoded' in self.df.columns]
        numerical_cols = ['Crop_Year', 'Area', 'Annual_Rainfall', 'Fertilizer', 'Pesticide', 'Temperature']
        self.features = numerical_cols + encoded_cols

        X = self.df[self.features]
        y = self.df[self.target]

        print(f"Features prepared. Shape: {X.shape}")
        return X, y

    def save_preprocessing_objects(self, save_path='./models/'):
        """
        Save the preprocessing objects (scaler and label encoders).

        Args:
            save_path (str): Directory to save the objects
        """
        os.makedirs(save_path, exist_ok=True)

        # Save scaler
        joblib.dump(self.scaler, os.path.join(save_path, 'scaler.pkl'))

        # Save label encoders
        for name, encoder in self.label_encoders.items():
            joblib.dump(encoder, os.path.join(save_path, f'{name.lower()}_encoder.pkl'))

        print("Preprocessing objects saved successfully")

    def preprocess(self):
        """
        Complete preprocessing pipeline.

        Returns:
            tuple: (X, y) processed features and target
        """
        self.load_data()
        if self.df is not None:
            self.clean_data()
            self.encode_categorical_features()
            self.scale_numerical_features()
            X, y = self.prepare_features()
            self.save_preprocessing_objects()
            return X, y
        else:
            return None, None

if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    X, y = preprocessor.preprocess()
    if X is not None:
        print("Preprocessing completed successfully!")
    else:
        print("Preprocessing failed!")