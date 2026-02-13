import os

# Configuration settings for the Twitter Sentiment Analysis App

class Config:
    # Model file paths
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'trained_model.sav')
    VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.sav')
    
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'twitter-sentiment-secret-key'
    DEBUG = True
    
    # Text processing settings
    MAX_TWEET_LENGTH = 280  # Standard Twitter character limit