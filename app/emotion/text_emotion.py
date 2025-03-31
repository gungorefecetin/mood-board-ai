from transformers import pipeline
from textblob import TextBlob
import numpy as np

class TextEmotionDetector:
    def __init__(self):
        # Initialize the emotion classifier pipeline
        self.classifier = pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-emotion",
            top_k=None
        )
        
    def get_emotion(self, text: str) -> dict:
        """
        Detect emotion from text using transformer model and TextBlob for sentiment.
        
        Args:
            text (str): Input text to analyze
        
        Returns:
            dict: Dictionary containing emotion and confidence scores
        """
        # Get emotion classification
        emotions = self.classifier(text)[0]
        
        # Get sentiment using TextBlob
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        
        # Convert emotions to dictionary format
        emotion_scores = {item['label']: item['score'] for item in emotions}
        
        # Get the primary emotion (highest score)
        primary_emotion = max(emotions, key=lambda x: x['score'])
        
        return {
            'primary_emotion': primary_emotion['label'],
            'confidence': primary_emotion['score'],
            'sentiment_score': sentiment_score,
            'all_emotions': emotion_scores
        }
    
    def get_emotion_category(self, text: str) -> str:
        """
        Get just the primary emotion category for the text.
        
        Args:
            text (str): Input text to analyze
        
        Returns:
            str: Primary emotion category
        """
        result = self.get_emotion(text)
        return result['primary_emotion'] 