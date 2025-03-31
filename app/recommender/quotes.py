import requests
from typing import List, Dict
import random

class QuoteRecommender:
    def __init__(self):
        """Initialize quote recommender with emotion-tag mappings."""
        self.base_url = "https://api.quotable.io"
        
        # Map emotions to relevant tags
        self.emotion_tags = {
            'happy': ['happiness', 'joy', 'inspirational', 'success'],
            'sad': ['hope', 'courage', 'perseverance', 'strength'],
            'angry': ['peace', 'calm', 'wisdom', 'patience'],
            'fear': ['courage', 'confidence', 'faith', 'strength'],
            'surprise': ['wisdom', 'change', 'philosophy'],
            'disgust': ['change', 'hope', 'wisdom'],
            'neutral': ['wisdom', 'life', 'philosophy']
        }
    
    def get_recommendations(self, emotion: str, limit: int = 3) -> List[Dict]:
        """
        Get quotes based on emotion.
        
        Args:
            emotion (str): Detected emotion
            limit (int): Number of quotes to return
            
        Returns:
            List[Dict]: List of quotes with author and tags
        """
        # Get relevant tags for the emotion
        tags = self.emotion_tags.get(emotion.lower(), self.emotion_tags['neutral'])
        
        # Randomly select one tag to get diverse quotes
        selected_tag = random.choice(tags)
        
        # Query the API
        params = {
            'tags': selected_tag,
            'limit': limit
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/quotes/random",
                params=params
            )
            
            if response.status_code == 200:
                quotes = response.json()
                return [{
                    'content': quote['content'],
                    'author': quote['author'],
                    'tags': quote['tags']
                } for quote in quotes]
            
        except requests.RequestException:
            pass
            
        # Fallback quotes if API fails
        fallback_quotes = {
            'happy': [
                {'content': 'Happiness is not something ready made. It comes from your own actions.',
                 'author': 'Dalai Lama', 'tags': ['happiness']},
            ],
            'sad': [
                {'content': 'Even the darkest night will end and the sun will rise.',
                 'author': 'Victor Hugo', 'tags': ['hope']},
            ],
            'angry': [
                {'content': 'For every minute you are angry you lose sixty seconds of happiness.',
                 'author': 'Ralph Waldo Emerson', 'tags': ['peace']},
            ],
            'fear': [
                {'content': 'Fear is only as deep as the mind allows.',
                 'author': 'Japanese Proverb', 'tags': ['courage']},
            ],
            'neutral': [
                {'content': 'Life is really simple, but we insist on making it complicated.',
                 'author': 'Confucius', 'tags': ['wisdom']},
            ]
        }
        
        return fallback_quotes.get(emotion.lower(), fallback_quotes['neutral']) 