"""
Script to fix model compatibility issues between different numpy versions.
This script attempts to recreate your model and vectorizer files to be compatible with current numpy version.
"""

import pickle
import joblib
import sys
import os

def fix_model_compatibility():
    print("Attempting to fix model compatibility issues...")
    
    # Paths to your original model files
    model_path = 'trained_model.sav'
    vectorizer_path = 'vectorizer.sav'
    
    # Check if files exist
    if not os.path.exists(model_path):
        print(f"Error: {model_path} not found!")
        return False
    
    if not os.path.exists(vectorizer_path):
        print(f"Error: {vectorizer_path} not found!")
        return False
    
    print("Found model files. Attempting to load with different protocols...")
    
    # Try to load with different pickle protocols
    model = None
    vectorizer = None
    
    # Try different approaches to load the model
    for protocol in [2, 3, 4, 5]:
        try:
            print(f"Trying to load model with protocol {protocol}...")
            with open(model_path, 'rb') as f:
                model = pickle.load(f, encoding='latin1')
            print(f"Model loaded successfully with protocol {protocol}")
            break
        except Exception as e:
            print(f"Failed with protocol {protocol}: {str(e)}")
            continue
    
    if model is None:
        try:
            print("Trying joblib.load...")
            model = joblib.load(model_path)
            print("Model loaded successfully with joblib")
        except Exception as e:
            print(f"Joblib also failed: {str(e)}")
    
    # Try to load the vectorizer
    for protocol in [2, 3, 4, 5]:
        try:
            print(f"Trying to load vectorizer with protocol {protocol}...")
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f, encoding='latin1')
            print(f"Vectorizer loaded successfully with protocol {protocol}")
            break
        except Exception as e:
            print(f"Vectorizer failed with protocol {protocol}: {str(e)}")
            continue
    
    if vectorizer is None:
        try:
            print("Trying joblib.load for vectorizer...")
            vectorizer = joblib.load(vectorizer_path)
            print("Vectorizer loaded successfully with joblib")
        except Exception as e:
            print(f"Vectorizer joblib also failed: {str(e)}")
    
    if model is None or vectorizer is None:
        print("\nERROR: Could not load either model or vectorizer.")
        print("This indicates that your model files are incompatible with the current environment.")
        print("\nSOLUTIONS:")
        print("1. Restore your original training environment with the same numpy version used to create the models")
        print("2. Recreate the models using the same training data and current environment")
        print("3. Use conda/virtual environment to match the original training environment")
        return False
    else:
        print("\nBoth model and vectorizer loaded successfully!")
        
        # Save them again with current environment
        backup_model = 'trained_model_backup.sav'
        backup_vectorizer = 'vectorizer_backup.sav'
        
        # Backup original files
        import shutil
        shutil.copy2(model_path, backup_model)
        shutil.copy2(vectorizer_path, backup_vectorizer)
        print(f"Backups created: {backup_model}, {backup_vectorizer}")
        
        # Save with current environment
        joblib.dump(model, model_path.replace('.sav', '_fixed.sav'))
        joblib.dump(vectorizer, vectorizer_path.replace('.sav', '_fixed.sav'))
        
        print(f"New compatible files created: {model_path.replace('.sav', '_fixed.sav')} and {vectorizer_path.replace('.sav', '_fixed.sav')}")
        print("\nYou can now rename these files back to the original names if they work correctly.")
        return True

if __name__ == "__main__":
    fix_model_compatibility()