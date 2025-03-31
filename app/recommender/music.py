import os
import base64
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class SpotifyRecommender:
    def __init__(self):
        """Initialize Spotify API client."""
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.token = None
        self.token_expiry = None
        
        # Emotion to music mapping
        self.emotion_genres = {
            'happy': ['pop', 'dance', 'happy'],
            'sad': ['sad', 'acoustic', 'piano'],
            'angry': ['rock', 'metal', 'intense'],
            'fear': ['ambient', 'classical', 'calm'],
            'surprise': ['electronic', 'experimental'],
            'disgust': ['punk', 'grunge', 'metal'],
            'neutral': ['indie', 'alternative', 'folk']
        }
        
    def get_token(self) -> None:
        """Get or refresh Spotify API access token."""
        if self.token and self.token_expiry > datetime.now():
            return
            
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={'Authorization': f'Basic {auth}'},
            data={'grant_type': 'client_credentials'}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data['access_token']
            self.token_expiry = datetime.now() + timedelta(seconds=data['expires_in'])
    
    def get_recommendations(self, emotion: str, limit: int = 5) -> List[Dict]:
        """
        Get music recommendations based on emotion.
        
        Args:
            emotion (str): Detected emotion
            limit (int): Number of recommendations to return
            
        Returns:
            List[Dict]: List of recommended tracks
        """
        self.get_token()
        
        if not self.token:
            return []
            
        # Get genres for the emotion
        seed_genres = self.emotion_genres.get(emotion.lower(), ['pop'])
        
        # Set mood-specific parameters
        params = {
            'limit': limit,
            'seed_genres': ','.join(seed_genres[:3]),  # Spotify allows max 5 seed values
        }
        
        # Add audio features based on emotion
        if emotion.lower() in ['happy', 'surprise']:
            params.update({
                'target_valence': 0.8,
                'target_energy': 0.8,
                'min_tempo': 120
            })
        elif emotion.lower() in ['sad', 'fear']:
            params.update({
                'target_valence': 0.3,
                'target_energy': 0.3,
                'max_tempo': 100
            })
        elif emotion.lower() == 'angry':
            params.update({
                'target_energy': 0.9,
                'target_valence': 0.4,
                'min_tempo': 130
            })
            
        response = requests.get(
            'https://api.spotify.com/v1/recommendations',
            headers={'Authorization': f'Bearer {self.token}'},
            params=params
        )
        
        if response.status_code != 200:
            return []
            
        tracks = response.json().get('tracks', [])
        
        return [{
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'preview_url': track['preview_url'],
            'external_url': track['external_urls']['spotify'],
            'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None
        } for track in tracks] 