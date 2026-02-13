"""
Model Setup Guide
===============

This file explains how to properly set up your trained model with the current environment.

ISSUE:
Your trained_model.sav and vectorizer.sav files were created with a different version of numpy,
which causes a ModuleNotFoundError: No module named 'numpy._core' when trying to load them.

SOLUTION:
To use your actual trained model, you need to recreate it in the current environment.

Steps to recreate your model properly:

1. RETRAIN YOUR MODEL WITH CURRENT ENVIRONMENT
   Use this code structure to save your model and vectorizer in a compatible way:

```python
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
# ... your model training code ...

# After training your model:
# Save the model and vectorizer using joblib (recommended for sklearn)
joblib.dump(your_trained_model, 'trained_model.sav')
joblib.dump(your_trained_vectorizer, 'vectorizer.sav')

# Make sure to use the same text preprocessing function you shared:
def stemming(content):
    import re
    from nltk.stem.porter import PorterStemmer
    from nltk.corpus import stopwords
    
    port_stem = PorterStemmer()
    stemming_content = re.sub('[^a-zA-Z]',' ',content)
    stemming_content = stemming_content.lower()
    stemming_content = stemming_content.split()
    stemming_content = [port_stem.stem(word) for word in stemming_content if not word in stopwords.words('english')]
    stemming_content = ' '.join(stemming_content)
    return stemming_content
```

2. ALTERNATIVE: Use a virtual environment with the original numpy version
   - Find out which numpy version was used originally
   - Create a virtual environment with that version
   - Train and save the model in that environment

3. IF YOU DON'T HAVE THE ORIGINAL TRAINING CODE:
   You can create a simple script to retrain with sample data following your preprocessing steps:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression  # or whatever algorithm you used
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk

# Download required NLTK data
nltk.download('stopwords')

def stemming(content):
    port_stem = PorterStemmer()
    stemming_content = re.sub('[^a-zA-Z]',' ',content)
    stemming_content = stemming_content.lower()
    stemming_content = stemming_content.split()
    stemming_content = [port_stem.stem(word) for word in stemming_content if not word in stopwords.words('english')]
    stemming_content = ' '.join(stemming_content)
    return stemming_content

# Load your dataset (you'll need to replace this with your actual data)
# df = pd.read_csv('your_twitter_dataset.csv')

# Example structure - adjust column names as needed
# df['processed_text'] = df['tweet_column'].apply(stemming)

# vectorizer = TfidfVectorizer(max_features=5000)  # adjust parameters as needed
# X = vectorizer.fit_transform(df['processed_text'])
# y = df['sentiment_column']  # 0 for negative, 1 for positive

# # Split the data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train your model (adjust algorithm as needed)
# model = LogisticRegression()  # or whatever algorithm you used
# model.fit(X_train, y_train)

# # Save the model and vectorizer
# joblib.dump(model, 'trained_model.sav')
# joblib.dump(vectorizer, 'vectorizer.sav')
```

Once you recreate your model files using the current environment, the application will work perfectly with your actual trained model and no fallback logic will be needed.
"""

print(__doc__)

# You can run this guide to understand the steps needed
if __name__ == "__main__":
    print("Please review the model setup guide above to properly recreate your model files.")
    print("After recreating your model with the current environment, your application will work with your actual trained model.")