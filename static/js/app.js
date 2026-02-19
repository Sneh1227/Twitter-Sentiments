document.addEventListener('DOMContentLoaded', function() {
    const tweetForm = document.getElementById('tweetForm');
    const tweetInput = document.getElementById('tweetInput');
    const currentCharCount = document.getElementById('currentCharCount');
    const maxCharCount = document.getElementById('maxCharCount');
    const predictBtn = document.getElementById('predictBtn');
    const btnText = document.getElementById('btnText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultContainer = document.getElementById('resultContainer');
    const resultContent = document.getElementById('resultContent');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    const sentimentIcon = document.getElementById('sentimentIcon');

    // Update character counter
    tweetInput.addEventListener('input', function() {
        const currentLength = tweetInput.value.length;
        currentCharCount.textContent = currentLength;
        
        // Change color if approaching limit
        if (currentLength > 250) {
            currentCharCount.style.color = '#ff6b6b';
        } else {
            currentCharCount.style.color = '#666';
        }
    });

    // Handle form submission
    tweetForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const tweetText = tweetInput.value.trim();
        
        if (!tweetText) {
            showError('Please enter some text to analyze.');
            return;
        }

        // Disable button and show loading spinner
        predictBtn.disabled = true;
        btnText.style.display = 'none';
        loadingSpinner.style.display = 'block';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: tweetText })
            });

            const data = await response.json();

            if (data.success) {
                displayResult(data.sentiment, data.message);
            } else {
                showError(data.error || 'An error occurred during prediction.');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please try again.');
        } finally {
            // Re-enable button and hide loading spinner
            predictBtn.disabled = false;
            btnText.style.display = 'inline';
            loadingSpinner.style.display = 'none';
        }
    });

    // Display result function
    function displayResult(sentiment, message) {
        // Reset classes
        resultContent.className = 'result-content';
        
        // Set content based on sentiment
        if (sentiment === 'positive') {
            resultContent.classList.add('positive-result');
            resultTitle.textContent = 'Positive Sentiment!';
            resultMessage.textContent = 'This tweet expresses a positive sentiment.';
            sentimentIcon.innerHTML = '😊';
        } else if (sentiment === 'negative') {
            resultContent.classList.add('negative-result');
            resultTitle.textContent = 'Negative Sentiment';
            resultMessage.textContent = 'This tweet expresses a negative sentiment.';
            sentimentIcon.innerHTML = '😞';
        } else {
            resultContent.classList.add('neutral-result');
            resultTitle.textContent = 'Neutral Sentiment';
            resultMessage.textContent = 'This tweet expresses a neutral sentiment.';
            sentimentIcon.innerHTML = '😐';
        }

        // Show result container
        resultContainer.style.display = 'block';
        
        // Scroll to results
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Show error message
    function showError(message) {
        resultContent.className = 'result-content';
        resultContent.classList.add('negative-result');
        resultTitle.textContent = 'Error';
        resultMessage.textContent = message;
        sentimentIcon.innerHTML = '❌';
        resultContainer.style.display = 'block';
        
        // Scroll to results
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Initialize character counter
    currentCharCount.textContent = tweetInput.value.length;
});