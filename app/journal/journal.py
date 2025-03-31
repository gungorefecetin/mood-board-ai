import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class MoodJournal:
    def __init__(self, journal_path: str = "app/data/mood_journal.json"):
        """
        Initialize mood journal.
        
        Args:
            journal_path (str): Path to the journal JSON file
        """
        self.journal_path = journal_path
        self.ensure_journal_exists()
    
    def ensure_journal_exists(self) -> None:
        """Create journal file if it doesn't exist."""
        os.makedirs(os.path.dirname(self.journal_path), exist_ok=True)
        if not os.path.exists(self.journal_path):
            with open(self.journal_path, 'w') as f:
                json.dump([], f)
    
    def add_entry(self, 
                  emotion: str,
                  confidence: float,
                  input_text: Optional[str] = None,
                  recommendations: Optional[Dict] = None) -> Dict:
        """
        Add a new mood journal entry.
        
        Args:
            emotion (str): Detected emotion
            confidence (float): Confidence score of emotion detection
            input_text (str, optional): User's input text
            recommendations (Dict, optional): Content recommendations
            
        Returns:
            Dict: The created journal entry
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion,
            'confidence': confidence,
            'input_text': input_text,
            'recommendations': recommendations
        }
        
        # Load existing entries
        entries = self.load_entries()
        
        # Add new entry
        entries.append(entry)
        
        # Save updated entries
        with open(self.journal_path, 'w') as f:
            json.dump(entries, f, indent=2)
            
        return entry
    
    def load_entries(self) -> List[Dict]:
        """
        Load all journal entries.
        
        Returns:
            List[Dict]: List of journal entries
        """
        try:
            with open(self.journal_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def get_emotion_trends(self) -> Dict:
        """
        Get emotion frequency and trends over time.
        
        Returns:
            Dict: Emotion statistics and trend data
        """
        entries = self.load_entries()
        if not entries:
            return {'frequencies': {}, 'timeline': None}
            
        # Convert entries to DataFrame
        df = pd.DataFrame(entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Calculate emotion frequencies
        frequencies = df['emotion'].value_counts().to_dict()
        
        # Create timeline data
        timeline = df.set_index('timestamp')['emotion'].resample('D').agg(lambda x: x.mode()[0] if len(x) > 0 else None)
        timeline = timeline.dropna()
        
        return {
            'frequencies': frequencies,
            'timeline': timeline.to_dict() if not timeline.empty else None
        }
    
    def create_visualization(self) -> Dict:
        """
        Create visualizations of mood data.
        
        Returns:
            Dict: Plotly figure data for emotion distribution and timeline
        """
        entries = self.load_entries()
        if not entries:
            return None
            
        df = pd.DataFrame(entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Emotion distribution pie chart
        emotion_counts = df['emotion'].value_counts()
        pie_fig = px.pie(
            values=emotion_counts.values,
            names=emotion_counts.index,
            title='Emotion Distribution'
        )
        
        # Emotion timeline
        timeline_fig = go.Figure()
        for emotion in df['emotion'].unique():
            emotion_data = df[df['emotion'] == emotion]
            timeline_fig.add_trace(go.Scatter(
                x=emotion_data['timestamp'],
                y=[emotion] * len(emotion_data),
                name=emotion,
                mode='markers'
            ))
        timeline_fig.update_layout(
            title='Emotion Timeline',
            yaxis_title='Emotion',
            xaxis_title='Date'
        )
        
        return {
            'distribution': pie_fig.to_dict(),
            'timeline': timeline_fig.to_dict()
        } 