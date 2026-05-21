import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
from preprocess import DataPreprocessor

class ModelTrainer:
    """
    Class for training and evaluating machine learning models for crop production prediction.
    """

    def __init__(self, X=None, y=None):
        """
        Initialize the model trainer.

        Args:
            X (pd.DataFrame): Feature matrix
            y (pd.Series): Target vector
        """
        self.X = X
        self.y = y
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.results = {}

    def split_data(self, test_size=0.2, random_state=42):
        """
        Split the data into training and testing sets.

        Args:
            test_size (float): Proportion of data to use for testing
            random_state (int): Random state for reproducibility
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state
        )
        print(f"Data split completed. Train shape: {self.X_train.shape}, Test shape: {self.X_test.shape}")

    def initialize_models(self):
        """
        Initialize the machine learning models.
        """
        self.models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Decision Tree': DecisionTreeRegressor(random_state=42),
            'XGBoost': XGBRegressor(random_state=42, verbosity=0)
        }
        print("Models initialized")

    def train_models(self):
        """
        Train all initialized models.
        """
        for name, model in self.models.items():
            model.fit(self.X_train, self.y_train)
            print(f"{name} trained successfully")

    def evaluate_models(self):
        """
        Evaluate all trained models using various metrics.

        Returns:
            pd.DataFrame: DataFrame containing evaluation results
        """
        for name, model in self.models.items():
            y_pred = model.predict(self.X_test)

            mae = mean_absolute_error(self.y_test, y_pred)
            mse = mean_squared_error(self.y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(self.y_test, y_pred)

            self.results[name] = {
                'MAE': mae,
                'MSE': mse,
                'RMSE': rmse,
                'R²': r2
            }

        results_df = pd.DataFrame(self.results).T
        print("Model evaluation completed")
        return results_df

    def get_best_model(self):
        """
        Get the best performing model based on R² score.

        Returns:
            tuple: (model_name, model_object)
        """
        best_model_name = max(self.results, key=lambda x: self.results[x]['R²'])
        best_model = self.models[best_model_name]
        print(f"Best model: {best_model_name} with R² = {self.results[best_model_name]['R²']:.4f}")
        return best_model_name, best_model

    def save_best_model(self, save_path='./models/crop_model.pkl'):
        """
        Save the best model to disk.

        Args:
            save_path (str): Path to save the model
        """
        _, best_model = self.get_best_model()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(best_model, save_path)
        print(f"Best model saved to {save_path}")

    def train_and_evaluate(self):
        """
        Complete training and evaluation pipeline.

        Returns:
            pd.DataFrame: Evaluation results
        """
        if self.X is None or self.y is None:
            print("Error: Features and target not provided. Run preprocessing first.")
            return None

        self.split_data()
        self.initialize_models()
        self.train_models()
        results_df = self.evaluate_models()
        self.save_best_model()
        return results_df

def main():
    """
    Main function to run the complete training pipeline.
    """
    # Preprocess data
    preprocessor = DataPreprocessor()
    X, y = preprocessor.preprocess()

    if X is not None and y is not None:
        # Train models
        trainer = ModelTrainer(X, y)
        results = trainer.train_and_evaluate()

        if results is not None:
            print("\nModel Evaluation Results:")
            print(results)
            print("\nTraining completed successfully!")
        else:
            print("Training failed!")
    else:
        print("Preprocessing failed. Cannot proceed with training.")

if __name__ == "__main__":
    main()