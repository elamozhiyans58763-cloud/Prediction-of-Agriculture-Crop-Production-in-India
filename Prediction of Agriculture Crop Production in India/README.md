# 🌾 Crop Production Prediction in India

A comprehensive machine learning-based web application for predicting crop production in India using agricultural and environmental factors.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Machine Learning Models](#machine-learning-models)
- [API Reference](#api-reference)
- [Project Architecture](#project-architecture)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project aims to help farmers, agricultural planners, and policymakers predict crop production based on various factors like rainfall, temperature, fertilizer usage, and more. The system uses multiple machine learning algorithms to provide accurate predictions and insights.

## ✨ Features

- **🔮 Accurate Predictions**: Predict crop production using advanced ML models
- **📊 Data Analysis**: Interactive visualizations and EDA
- **🌱 Crop Recommendations**: Smart crop suggestions based on conditions
- **💡 Fertilizer Recommendations**: Optimized fertilizer usage suggestions
- **🎨 Modern UI**: Attractive and responsive Streamlit interface
- **📈 Performance Metrics**: Comprehensive model evaluation
- **💾 Model Persistence**: Save and load trained models
- **🔍 Data Insights**: Correlation analysis and trend visualization

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Libraries**:
  - Data Processing: Pandas, NumPy
  - Machine Learning: Scikit-learn, XGBoost
  - Visualization: Matplotlib, Seaborn
  - Web Framework: Streamlit
  - Model Persistence: Joblib
- **Frontend**: Streamlit (with HTML/CSS fallback)

## 📁 Project Structure

```
Crop_Production_Prediction/
│
├── dataset/
│   └── crop_production.csv          # Agricultural dataset
│
├── models/
│   ├── crop_model.pkl              # Trained ML model
│   ├── scaler.pkl                  # Feature scaler
│   └── *_encoder.pkl               # Label encoders
│
├── notebooks/
│   └── data_analysis.ipynb         # EDA and model training notebook
│
├── app/
│   ├── app.py                      # Main Streamlit application
│   ├── prediction.py               # Prediction logic and visualizations
│   └── utils.py                    # Utility functions
│
├── templates/
│   └── index.html                  # HTML template (fallback)
│
├── static/
│   └── style.css                   # CSS styles
│
├── preprocess.py                   # Data preprocessing script
├── train_model.py                  # Model training script
├── main.py                         # Main execution script
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step-by-Step Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd "Prediction of Agriculture Crop Production in India"
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the main script** to preprocess data and train models:
   ```bash
   python main.py
   ```

## 📖 Usage

### Running the Application

1. **Start the Flask web app**:
   ```bash
   python run.py
   ```

2. **Open your browser** and navigate to `http://127.0.0.1:5000` in Chrome.

### Using the Application

1. **Prediction Page**: Input agricultural parameters and get production predictions
2. **Data Analysis Page**: View visualizations and dataset insights
3. **Crop Recommendations**: Get crop suggestions based on conditions
4. **About Page**: Learn more about the project

### Command Line Usage

- **Preprocess data only**:
  ```bash
  python preprocess.py
  ```

- **Train models only**:
  ```bash
  python train_model.py
  ```

- **Run Jupyter notebook**:
  ```bash
  jupyter notebook notebooks/data_analysis.ipynb
  ```

## 📊 Dataset

### Description

The dataset contains agricultural data from various states in India with the following features:

- **State_Name**: Name of the Indian state
- **District_Name**: Name of the district
- **Crop_Year**: Year of cultivation
- **Season**: Kharif, Rabi, or Whole Year
- **Crop**: Type of crop (Rice, Wheat, Maize, etc.)
- **Area**: Area under cultivation (hectares)
- **Annual_Rainfall**: Annual rainfall in mm
- **Fertilizer**: Fertilizer usage in kg/ha
- **Pesticide**: Pesticide usage in kg/ha
- **Temperature**: Average temperature in °C
- **Production**: Crop production in tons (target variable)

### Data Preprocessing

- Handle missing values
- Encode categorical variables (State, District, Season, Crop)
- Scale numerical features
- Split into training and testing sets (80-20 ratio)

## 🤖 Machine Learning Models

The system implements and compares four regression models:

### 1. Linear Regression
- Baseline model
- Assumes linear relationship between features and target

### 2. Random Forest Regressor
- Ensemble method using multiple decision trees
- Handles non-linear relationships and feature interactions

### 3. Decision Tree Regressor
- Tree-based model
- Easy to interpret and visualize

### 4. XGBoost Regressor
- Gradient boosting algorithm
- Often provides highest accuracy
- Handles missing values internally

### Model Evaluation Metrics

- **MAE** (Mean Absolute Error)
- **MSE** (Mean Squared Error)
- **RMSE** (Root Mean Squared Error)
- **R² Score** (Coefficient of Determination)

## 🔧 API Reference

### PredictionUtils Class

```python
from app.utils import PredictionUtils

# Initialize
utils = PredictionUtils()

# Make prediction
input_data = {
    'State_Name': 'Maharashtra',
    'Crop_Year': 2023,
    'Season': 'Kharif',
    'Crop': 'Rice',
    'Area': 10.0,
    'Annual_Rainfall': 1200.0,
    'Fertilizer': 50.0,
    'Pesticide': 10.0,
    'Temperature': 25.0
}
prediction = utils.predict_production(input_data)
```

### CropPredictor Class

```python
from app.prediction import CropPredictor

predictor = CropPredictor()

# Get recommendations
crops = predictor.get_crop_recommendations('Maharashtra', 'Kharif', 1200, 25)
fertilizer = predictor.get_fertilizer_recommendation('Rice', 10.0)
```

## 🏗️ Project Architecture

### Data Flow

1. **Data Ingestion**: Load CSV dataset
2. **Preprocessing**: Clean, encode, and scale data
3. **Model Training**: Train multiple ML models
4. **Model Evaluation**: Compare performance metrics
5. **Model Selection**: Choose best performing model
6. **Web Application**: Deploy interactive prediction interface

### Modular Design

- **preprocess.py**: Data preprocessing utilities
- **train_model.py**: Model training and evaluation
- **app/utils.py**: Prediction utilities
- **app/prediction.py**: Prediction logic and recommendations
- **app/app.py**: Streamlit web interface

## 🔮 Future Enhancements

### Planned Features

- [ ] **Weather API Integration**: Real-time weather data
- [ ] **Geospatial Analysis**: Location-based insights
- [ ] **Time Series Forecasting**: Seasonal predictions
- [ ] **Mobile App**: React Native application
- [ ] **REST API**: Backend API for external integrations
- [ ] **Advanced ML**: Deep learning models (LSTM, CNN)
- [ ] **Multi-language Support**: Regional language interfaces
- [ ] **Historical Analysis**: Long-term trend analysis
- [ ] **Soil Data Integration**: Soil quality parameters
- [ ] **Economic Analysis**: Cost-benefit analysis

### Technical Improvements

- [ ] **Model Interpretability**: SHAP values and feature importance
- [ ] **Hyperparameter Tuning**: Automated model optimization
- [ ] **Cross-validation**: Robust model validation
- [ ] **Ensemble Methods**: Model stacking and blending
- [ ] **A/B Testing**: Model performance comparison
- [ ] **CI/CD Pipeline**: Automated testing and deployment

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to functions
- Write unit tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset source: Agricultural statistics from various Indian states
- Inspired by agricultural technology initiatives
- Built with open-source machine learning libraries

## 📞 Contact

For questions or support, please open an issue on GitHub or contact the development team.

---

**Happy Farming! 🌾🚜**