"""
Database module for Smart Agriculture System
Supports both MongoDB and MySQL
"""

import os
from pymongo import MongoClient
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Database:
    def __init__(self, db_type='mongodb', config=None):
        """
        Initialize database connection
        
        Args:
            db_type: 'mongodb' or 'mysql'
            config: Database configuration dictionary
        """
        self.db_type = db_type
        self.config = config or self._get_default_config()
        self.connection = None
        self.connect()
    
    def _get_default_config(self):
        """Get default configuration from environment variables"""
        if self.db_type == 'mongodb':
            return {
                'host': os.getenv('MONGO_HOST', 'localhost'),
                'port': int(os.getenv('MONGO_PORT', 27017)),
                'database': os.getenv('MONGO_DB', 'smart_agriculture'),
                'username': os.getenv('MONGO_USER', None),
                'password': os.getenv('MONGO_PASSWORD', None)
            }
        else:  # mysql
            return {
                'host': os.getenv('MYSQL_HOST', 'localhost'),
                'user': os.getenv('MYSQL_USER', 'root'),
                'password': os.getenv('MYSQL_PASSWORD', ''),
                'database': os.getenv('MYSQL_DB', 'smart_agriculture'),
                'port': int(os.getenv('MYSQL_PORT', 3306))
            }
    
    def connect(self):
        """Establish database connection"""
        try:
            if self.db_type == 'mongodb':
                if self.config['username'] and self.config['password']:
                    uri = f"mongodb://{self.config['username']}:{self.config['password']}@{self.config['host']}:{self.config['port']}"
                else:
                    uri = f"mongodb://{self.config['host']}:{self.config['port']}"
                
                self.connection = MongoClient(uri)
                self.db = self.connection[self.config['database']]
            else:  # mysql
                self.connection = mysql.connector.connect(
                    host=self.config['host'],
                    user=self.config['user'],
                    password=self.config['password'],
                    database=self.config['database'],
                    port=self.config['port']
                )
            print(f"✓ {self.db_type.upper()} connection successful")
        except Error as e:
            print(f"✗ Database connection error: {e}")
            self.connection = None
    
    def create_users_table(self):
        """Create users table/collection"""
        if self.db_type == 'mongodb':
            self.db.users.create_index([('username', 1)], unique=True)
            self.db.users.create_index([('email', 1)], unique=True)
        else:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    phone VARCHAR(15),
                    location VARCHAR(100),
                    farm_size FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()
    
    def create_predictions_table(self):
        """Create predictions table/collection"""
        if self.db_type == 'mongodb':
            self.db.predictions.create_index([('user_id', 1)])
            self.db.predictions.create_index([('created_at', 1)])
        else:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    state VARCHAR(50),
                    district VARCHAR(50),
                    crop VARCHAR(50),
                    season VARCHAR(20),
                    year INT,
                    predicted_production FLOAT,
                    confidence FLOAT,
                    input_data JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            self.connection.commit()
    
    def create_recommendations_table(self):
        """Create recommendations table/collection"""
        if self.db_type == 'mongodb':
            self.db.recommendations.create_index([('user_id', 1)])
        else:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    type VARCHAR(50),
                    recommendation_text TEXT,
                    confidence FLOAT,
                    metadata JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            self.connection.commit()
    
    def create_disease_detection_table(self):
        """Create disease detection results table/collection"""
        if self.db_type == 'mongodb':
            self.db.disease_detection.create_index([('user_id', 1)])
        else:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS disease_detection (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    image_path VARCHAR(255),
                    detected_disease VARCHAR(100),
                    confidence FLOAT,
                    treatment_suggestions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            self.connection.commit()
    
    def init_all_tables(self):
        """Initialize all tables/collections"""
        self.create_users_table()
        self.create_predictions_table()
        self.create_recommendations_table()
        self.create_disease_detection_table()
        print("✓ All tables initialized successfully")
    
    def insert_user(self, user_data):
        """Insert new user"""
        if self.db_type == 'mongodb':
            user_data['created_at'] = datetime.utcnow()
            result = self.db.users.insert_one(user_data)
            return str(result.inserted_id)
        else:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO users (username, email, password, phone, location, farm_size)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                user_data.get('username'),
                user_data.get('email'),
                user_data.get('password'),
                user_data.get('phone'),
                user_data.get('location'),
                user_data.get('farm_size')
            ))
            self.connection.commit()
            return cursor.lastrowid
    
    def get_user(self, username):
        """Get user by username"""
        if self.db_type == 'mongodb':
            return self.db.users.find_one({'username': username})
        else:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            return cursor.fetchone()
    
    def save_prediction(self, user_id, prediction_data):
        """Save prediction result"""
        if self.db_type == 'mongodb':
            prediction_data['user_id'] = user_id
            prediction_data['created_at'] = datetime.utcnow()
            result = self.db.predictions.insert_one(prediction_data)
            return str(result.inserted_id)
        else:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO predictions (user_id, state, district, crop, season, year,
                    predicted_production, confidence, input_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                user_id,
                prediction_data.get('state'),
                prediction_data.get('district'),
                prediction_data.get('crop'),
                prediction_data.get('season'),
                prediction_data.get('year'),
                prediction_data.get('predicted_production'),
                prediction_data.get('confidence'),
                str(prediction_data)
            ))
            self.connection.commit()
            return cursor.lastrowid
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
