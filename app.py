from flask import Flask, render_template, request, jsonify
from config import Config
from sentiment_predictor import predictor

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle sentiment prediction request"""
    try:
        # Get the tweet text from the request
        data = request.get_json()
        tweet_text = data.get('text', '').strip()
        
        if not tweet_text:
            return jsonify({
                'success': False,
                'error': 'Empty tweet text provided'
            }), 400
        
        # Check if text is too long
        if len(tweet_text) > Config.MAX_TWEET_LENGTH:
            return jsonify({
                'success': False,
                'error': f'Tweet is too long. Maximum {Config.MAX_TWEET_LENGTH} characters allowed.'
            }), 400
        
        # Make prediction using the sentiment predictor
        sentiment, confidence = predictor.predict_sentiment(tweet_text)
        
        # Return the prediction result
        return jsonify({
            'success': True,
            'sentiment': sentiment,
            'confidence': float(confidence),
            'message': f'The sentiment of the tweet is {sentiment} with {confidence:.2f} confidence'
        })
        
    except Exception as e:
        # Handle any errors during prediction
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)