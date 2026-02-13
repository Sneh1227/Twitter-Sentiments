"""
Script to help regenerate your vectorizer properly if it's not fitted correctly.
"""

import joblib
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk

# Download required NLTK data if not already present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def check_and_fix_vectorizer():
    """
    Checks if the vectorizer is properly fitted and suggests fixes if not
    """
    try:
        # Load the vectorizer
        vectorizer = joblib.load('vectorizer.sav')
        
        # Try to use the vectorizer to see if it's properly fitted
        sample_text = ["This is a sample text for testing"]
        
        try:
            # This will fail if the vectorizer hasn't been fitted
            result = vectorizer.transform(sample_text)
            print("✓ Vectorizer is properly fitted and working!")
            return True
        except ValueError as e:
            print(f"✗ Vectorizer is not properly fitted: {e}")
            print("\nTo fix this issue, you need to retrain your vectorizer properly:")
            print("""
Steps to properly save your vectorizer:

1. Fit the vectorizer on your training data:
   ```python
   from sklearn.feature_extraction.text import TfidfVectorizer
   
   # Assuming you have processed training texts
   vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')  # Adjust parameters as needed
   X_train_vectors = vectorizer.fit(train_texts)  # Note: use fit() or fit_transform()
   
   # Then save it:
   joblib.dump(vectorizer, 'vectorizer.sav')
   ```

2. Make sure when training, you use:
   - vectorizer.fit(train_texts) OR 
   - vectorizer.fit_transform(train_texts)
   
   NOT just vectorizer.transform(train_texts)
""")
            return False
    except Exception as e:
        print(f"Error loading vectorizer: {e}")
        return False

def regenerate_sample_vectorizer():
    """
    Creates a sample vectorizer to demonstrate proper saving
    """
    print("\nCreating a sample vectorizer to demonstrate proper usage...")
    
    # Sample training data (you would use your actual training data)
    sample_training_texts = [
        "I love this product it's amazing",
        "This is terrible and disappointing", 
        "Great service and friendly staff",
        "Worst experience ever had",
        "Absolutely fantastic and wonderful"
    ]
    
    # Process the training texts using your normalization function
    processed_training_texts = [normalize_text(text) for text in sample_training_texts]
    
    # Create and fit the vectorizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')  # Adjust max_features as needed
    vectorizer.fit(processed_training_texts)  # This is the key - fit() must be called!
    
    # Save the fitted vectorizer
    joblib.dump(vectorizer, 'vectorizer_fixed.sav')
    print("Sample fixed vectorizer saved as 'vectorizer_fixed.sav'")
    print("Replace your original 'vectorizer.sav' with this file if needed.")

def normalize_text(content):
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
    stemmer = PorterStemmer()
    stemmed_content = [
        stemmer.stem(word) 
        for word in stemmed_content 
        if word not in stopwords.words('english')
    ]
    
    # Join the words back into a string
    stemmed_content = ' '.join(stemmed_content)
    
    return stemmed_content

if __name__ == "__main__":
    print("Checking your vectorizer...")
    is_working = check_and_fix_vectorizer()
    
    if not is_working:
        regenerate_sample_vectorizer()
    
    print("\nRemember: When you save your vectorizer, make sure you call:")
    print("- vectorizer.fit(training_texts) OR")
    print("- vectorizer.fit_transform(training_texts)")
    print("before saving with joblib.dump(vectorizer, 'vectorizer.sav')")