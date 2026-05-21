"""
Disease Detection Module using CNN
Detects plant diseases from leaf images
"""

import numpy as np
import cv2
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from typing import Dict, Tuple

class DiseaseDetector:
    def __init__(self, model_path: str = None):
        """
        Initialize disease detector
        
        Args:
            model_path: Path to pre-trained model
        """
        self.diseases = {
            'Leaf Blight': {
                'description': 'Fungal disease causing brown/black spots on leaves',
                'treatment': [
                    'Apply copper fungicide spray',
                    'Improve air circulation',
                    'Remove infected leaves',
                    'Avoid overhead watering'
                ],
                'affected_crops': ['Rice', 'Wheat', 'Maize'],
                'season': ['Monsoon', 'Post-monsoon'],
                'severity': 'High'
            },
            'Rust': {
                'description': 'Fungal disease with orange/red powdery spores',
                'treatment': [
                    'Apply sulfur or copper-based fungicide',
                    'Ensure adequate plant spacing',
                    'Remove affected leaves',
                    'Maintain proper humidity (below 70%)'
                ],
                'affected_crops': ['Wheat', 'Groundnut', 'Soybean'],
                'season': ['Rabi'],
                'severity': 'Medium'
            },
            'Powdery Mildew': {
                'description': 'White powdery coating on leaves and stems',
                'treatment': [
                    'Apply sulfur dust or spray',
                    'Improve air circulation',
                    'Remove infected plant parts',
                    'Avoid excess nitrogen fertilizer'
                ],
                'affected_crops': ['Wheat', 'Squash', 'Cucumber'],
                'season': ['All'],
                'severity': 'Medium'
            },
            'Bacterial Spot': {
                'description': 'Small dark spots with yellow halos',
                'treatment': [
                    'Apply copper bactericide',
                    'Remove infected leaves',
                    'Improve drainage',
                    'Use disease-free seeds'
                ],
                'affected_crops': ['Cotton', 'Tomato', 'Pepper'],
                'season': ['Monsoon'],
                'severity': 'High'
            },
            'Early Blight': {
                'description': 'Brown circular spots on leaves with concentric rings',
                'treatment': [
                    'Remove lower infected leaves',
                    'Apply mancozeb fungicide',
                    'Improve air circulation',
                    'Mulch around plants'
                ],
                'affected_crops': ['Tomato', 'Potato'],
                'season': ['Monsoon', 'Post-monsoon'],
                'severity': 'Medium'
            },
            'Healthy': {
                'description': 'No disease detected',
                'treatment': [],
                'affected_crops': [],
                'season': [],
                'severity': 'None'
            }
        }
        
        self.model_path = model_path
        self.model = None
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """Load pre-trained model"""
        try:
            self.model = keras.models.load_model(model_path)
            print(f"✓ Model loaded from {model_path}")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
    
    def preprocess_image(self, image_path: str, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """
        Preprocess image for model prediction
        
        Args:
            image_path: Path to image file
            target_size: Target image size
        
        Returns:
            Preprocessed image array
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize
            image = cv2.resize(image, target_size)
            
            # Normalize
            image = image.astype('float32') / 255.0
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
        except Exception as e:
            print(f"✗ Error preprocessing image: {e}")
            return None
    
    def detect_disease(self, image_path: str, confidence_threshold: float = 0.5):
        """
        Detect disease in leaf image
        
        Args:
            image_path: Path to leaf image
            confidence_threshold: Minimum confidence for detection
        
        Returns:
            Detection results with disease info
        """
        try:
            # If no model is loaded, use rule-based detection
            if self.model is None:
                return self._simple_disease_detection(image_path)
            
            # Preprocess image
            preprocessed = self.preprocess_image(image_path)
            if preprocessed is None:
                return {'error': 'Could not process image'}
            
            # Make prediction
            predictions = self.model.predict(preprocessed, verbose=0)
            
            # Get top prediction
            disease_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][disease_idx])
            
            disease_list = list(self.diseases.keys())
            detected_disease = disease_list[disease_idx] if disease_idx < len(disease_list) else 'Unknown'
            
            if confidence < confidence_threshold:
                detected_disease = 'Inconclusive'
                confidence = 0.0
            
            return {
                'detected_disease': detected_disease,
                'confidence': confidence,
                'all_predictions': {disease_list[i]: float(predictions[0][i]) for i in range(len(disease_list))},
                'disease_info': self.diseases.get(detected_disease, {}),
                'image_path': image_path,
                'timestamp': str(np.datetime64('today'))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _simple_disease_detection(self, image_path: str) -> Dict:
        """Simple rule-based disease detection for demo"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {'error': 'Could not read image'}
            
            # Convert to HSV for color analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Count different colors
            green = cv2.inRange(hsv, (36, 25, 25), (86, 255, 255))
            yellow = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255))
            brown = cv2.inRange(hsv, (8, 100, 100), (20, 255, 255))
            white = cv2.inRange(hsv, (0, 0, 200), (255, 50, 255))
            
            green_pixels = np.sum(green) / 255
            yellow_pixels = np.sum(yellow) / 255
            brown_pixels = np.sum(brown) / 255
            white_pixels = np.sum(white) / 255
            
            total_pixels = image.shape[0] * image.shape[1]
            
            # Determine disease based on color distribution
            if green_pixels > total_pixels * 0.7:
                disease = 'Healthy'
                confidence = 0.85
            elif white_pixels > total_pixels * 0.3:
                disease = 'Powdery Mildew'
                confidence = 0.75
            elif brown_pixels > total_pixels * 0.2:
                disease = 'Leaf Blight'
                confidence = 0.70
            elif yellow_pixels > total_pixels * 0.2:
                disease = 'Rust'
                confidence = 0.65
            else:
                disease = 'Healthy'
                confidence = 0.60
            
            return {
                'detected_disease': disease,
                'confidence': confidence,
                'disease_info': self.diseases.get(disease, {}),
                'image_path': image_path,
                'method': 'Color-based detection',
                'timestamp': str(np.datetime64('today'))
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_treatment(self, disease: str) -> Dict:
        """Get treatment suggestions for disease"""
        if disease in self.diseases:
            return {
                'disease': disease,
                'description': self.diseases[disease]['description'],
                'treatment_steps': self.diseases[disease]['treatment'],
                'affected_crops': self.diseases[disease]['affected_crops'],
                'season': self.diseases[disease]['season'],
                'severity': self.diseases[disease]['severity'],
                'prevention_tips': self._get_prevention_tips(disease)
            }
        return {'error': f'Disease not found: {disease}'}
    
    def _get_prevention_tips(self, disease: str) -> list:
        """Get prevention tips"""
        prevention = {
            'Leaf Blight': [
                'Use disease-resistant varieties',
                'Maintain field hygiene',
                'Crop rotation for 2-3 years',
                'Avoid high nitrogen fertilizer'
            ],
            'Rust': [
                'Sow resistant varieties',
                'Avoid planting too close',
                'Monitor regularly from flowering stage',
                'Clear weeds from field'
            ],
            'Powdery Mildew': [
                'Ensure good air circulation',
                'Avoid over-watering',
                'Remove infected plant parts early',
                'Maintain balanced nitrogen levels'
            ],
            'Bacterial Spot': [
                'Use disease-free seeds',
                'Implement proper sanitation',
                'Avoid overhead irrigation',
                'Practice crop rotation'
            ]
        }
        return prevention.get(disease, ['Monitor crop regularly', 'Maintain good hygiene'])

# Initialize
disease_detector = DiseaseDetector()
