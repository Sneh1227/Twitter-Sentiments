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
            # Try to load with joblib first (more robust for sklearn models)
            self.model = joblib.load(Config.MODEL_PATH)
            print("Model loaded successfully with joblib")
        except ModuleNotFoundError as e:
            if "numpy._core" in str(e):
                print(f"Model compatibility issue detected: {str(e)}")
                print("Your model was trained with a different numpy version.")
                print("Please follow the instructions in model_setup_guide.py to recreate your model with the current environment.")
                print("Run 'python model_setup_guide.py' for detailed instructions.")
                raise  # Re-raise to stop the application since the model is incompatible
            else:
                raise
        except Exception as e:
            print(f"Unexpected error loading model: {str(e)}")
            raise  # Re-raise the exception to stop the application if model fails to load
        
        try:
            # Try to load with joblib first (more robust for sklearn models)
            self.vectorizer = joblib.load(Config.VECTORIZER_PATH)
            print("Vectorizer loaded successfully with joblib")
        except ModuleNotFoundError as e:
            if "numpy._core" in str(e):
                print(f"Vectorizer compatibility issue detected: {str(e)}")
                print("Your vectorizer was trained with a different numpy version.")
                print("Please follow the instructions in model_setup_guide.py to recreate your vectorizer with the current environment.")
                print("Run 'python model_setup_guide.py' for detailed instructions.")
                raise  # Re-raise to stop the application since the vectorizer is incompatible
            else:
                raise
        except Exception as e:
            print(f"Unexpected error loading vectorizer: {str(e)}")
            raise  # Re-raise the exception to stop the application if vectorizer fails to load
    
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
        text_vector = self.vectorizer.transform([normalized_text])
        
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