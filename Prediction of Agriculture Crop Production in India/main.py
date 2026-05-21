#!/usr/bin/env python3
"""
Main script for the Crop Production Prediction project.
This script runs the complete pipeline: data preprocessing, model training, and launches the Streamlit app.
"""

import os
import subprocess
import sys

def run_preprocessing():
    """
    Run the data preprocessing script.
    """
    print("Running data preprocessing...")
    result = subprocess.run([sys.executable, 'preprocess.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Preprocessing completed successfully!")
        print(result.stdout)
    else:
        print("Preprocessing failed!")
        print(result.stderr)
        return False
    return True

def run_training():
    """
    Run the model training script.
    """
    print("Running model training...")
    result = subprocess.run([sys.executable, 'train_model.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Model training completed successfully!")
        print(result.stdout)
    else:
        print("Model training failed!")
        print(result.stderr)
        return False
    return True

def run_streamlit_app():
    """
    Launch the Streamlit web application.
    """
    print("Launching Streamlit app...")
    try:
        # Change to app directory
        os.chdir('app')
        # Run streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
    except KeyboardInterrupt:
        print("Streamlit app stopped by user.")
    except Exception as e:
        print(f"Error running Streamlit app: {e}")

def check_requirements():
    """
    Check if required packages are installed.
    """
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'scikit-learn': 'sklearn',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'streamlit': 'streamlit',
        'joblib': 'joblib',
        'xgboost': 'xgboost'
    }

    missing_packages = []
    for package, module_name in required_packages.items():
        try:
            __import__(module_name)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("Missing required packages:", missing_packages)
        print("Please install them using: pip install -r requirements.txt")
        return False

    print("All required packages are installed.")
    return True

def main():
    """
    Main function to run the complete project pipeline.
    """
    print("Welcome to Crop Production Prediction System")
    print("=" * 50)

    # Check requirements
    if not check_requirements():
        return

    # Run preprocessing
    if not run_preprocessing():
        return

    # Run training
    if not run_training():
        return

    # Ask user if they want to run the app
    response = input("Do you want to launch the Streamlit web app? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        run_streamlit_app()
    else:
        print("You can run the app later using: streamlit run app/app.py")

    print("\nThank you for using Crop Production Prediction System!")

if __name__ == "__main__":
    main()