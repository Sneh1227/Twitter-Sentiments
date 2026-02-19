import re
import pickle
import joblib
import warnings
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from config import Config

class SentimentPredictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.stemmer = PorterStemmer()
        self.load_models()
    
    def load_models(self):
        """Load the trained model and vectorizer from disk"""
        try:
            # Load the model
            self.model = joblib.load(Config.MODEL_PATH)
            print("Model loaded successfully with joblib")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
        
        try:
            # Load the vectorizer
            self.vectorizer = joblib.load(Config.VECTORIZER_PATH)
            print("Vectorizer loaded successfully with joblib")
        except Exception as e:
            print(f"Error loading vectorizer: {str(e)}")
            raise
    
    def normalize_text(self, content):
        """
        Normalize the text by removing special characters, converting to lowercase,
        removing stopwords, and applying stemming as per the user's function
        """
        # Remove special characters and keep only alphabets
        stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
        
        # Convert to lowercase
        stemmed_content = stemmed_content.lower()
        
        # Split into words
        stemmed_content = stemmed_content.split()
        
        # Apply stemming and remove stopwords
        stemmed_content = [
            self.stemmer.stem(word) 
            for word in stemmed_content 
            if word not in stopwords.words('english')
        ]
        
        # Join the words back into a string
        stemmed_content = ' '.join(stemmed_content)
        
        return stemmed_content
    
    def predict_sentiment(self, text):
        """
        Predict the sentiment of the given text
        Returns: sentiment ('positive' or 'negative') and confidence score
        """
        # Normalize the input text
        normalized_text = self.normalize_text(text)
        
        # Transform the text using the vectorizer
        # Handle potential issue with unfitted vectorizer
        try:
            text_vector = self.vectorizer.transform([normalized_text])
        except ValueError as e:
            if "VocabularyException" in str(e) or "not fitted" in str(e).lower():
                # This might happen if the vectorizer vocabulary is not properly saved
                # Try fitting on the input or handling differently
                # For now, we'll return an error message
                raise ValueError(f"Vectorizer not properly fitted: {str(e)}. Please retrain your vectorizer and save it properly using joblib.")
            else:
                raise
        
        # Make prediction
        prediction = self.model.predict(text_vector)[0]
        prediction_proba = self.model.predict_proba(text_vector)[0]
        
        # Determine the sentiment and confidence
        if prediction == 1:
            sentiment = 'positive'
            confidence = max(prediction_proba)
        else:
            sentiment = 'negative'
            confidence = max(prediction_proba)
        
        return sentiment, confidence

# Global predictor instance
predictor = SentimentPredictor()