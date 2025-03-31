import os
import requests
from typing import List, Dict

class MovieRecommender:
    def __init__(self):
        """Initialize TMDB API client."""
        self.api_key = os.getenv('TMDB_API_KEY')
        self.base_url = 'https://api.themoviedb.org/3'
        
        # Emotion to genre/keyword mapping
        self.emotion_mapping = {
            'happy': {
                'genres': [35, 10751],  # Comedy, Family
                'keywords': ['feel-good', 'uplifting', 'comedy']
            },
            'sad': {
                'genres': [18, 10749],  # Drama, Romance
                'keywords': ['emotional', 'touching', 'heartwarming']
            },
            'angry': {
                'genres': [28, 12],  # Action, Adventure
                'keywords': ['revenge', 'justice', 'triumph']
            },
            'fear': {
                'genres': [27, 53],  # Horror, Thriller
                'keywords': ['suspense', 'supernatural', 'mystery']
            },
            'surprise': {
                'genres': [878, 14],  # Science Fiction, Fantasy
                'keywords': ['plot-twist', 'mind-bending', 'unexpected']
            },
            'disgust': {
                'genres': [27, 53],  # Horror, Thriller
                'keywords': ['disturbing', 'controversial', 'dark']
            },
            'neutral': {
                'genres': [18, 99],  # Drama, Documentary
                'keywords': ['thought-provoking', 'inspiring', 'meaningful']
            }
        }
    
    def get_recommendations(self, emotion: str, limit: int = 5) -> List[Dict]:
        """
        Get movie recommendations based on emotion.
        
        Args:
            emotion (str): Detected emotion
            limit (int): Number of recommendations to return
            
        Returns:
            List[Dict]: List of recommended movies
        """
        if not self.api_key:
            return []
            
        emotion_data = self.emotion_mapping.get(emotion.lower(), self.emotion_mapping['neutral'])
        
        # Get movies by genre
        params = {
            'api_key': self.api_key,
            'with_genres': ','.join(map(str, emotion_data['genres'])),
            'sort_by': 'popularity.desc',
            'page': 1
        }
        
        response = requests.get(
            f'{self.base_url}/discover/movie',
            params=params
        )
        
        if response.status_code != 200:
            return []
            
        movies = response.json().get('results', [])[:limit]
        
        # Get additional details for each movie
        detailed_movies = []
        for movie in movies:
            movie_id = movie['id']
            details_response = requests.get(
                f'{self.base_url}/movie/{movie_id}',
                params={'api_key': self.api_key}
            )
            
            if details_response.status_code == 200:
                details = details_response.json()
                detailed_movies.append({
                    'title': details['title'],
                    'overview': details['overview'],
                    'release_date': details['release_date'],
                    'rating': details['vote_average'],
                    'poster_path': f"https://image.tmdb.org/t/p/w500{details['poster_path']}" if details['poster_path'] else None,
                    'genres': [genre['name'] for genre in details['genres']],
                    'runtime': details['runtime'],
                    'tmdb_url': f"https://www.themoviedb.org/movie/{movie_id}"
                })
                
        return detailed_movies 