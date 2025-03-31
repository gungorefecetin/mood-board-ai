# MoodBoard AI – Emotion-Aware Content Recommender

An AI-powered application that detects your mood and provides personalized content recommendations including music, movies, quotes, and articles.

## Features

- 🎭 Emotion Detection through text and webcam
- 🎵 Music recommendations based on mood
- 🎬 Movie suggestions that match your emotional state
- 💭 Inspirational quotes
- 📰 Relevant articles and content
- 📊 Personal mood tracking and visualization
- 🎨 Beautiful and intuitive user interface

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mood-board.git
cd mood-board
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
TMDB_API_KEY=your_tmdb_api_key
NEWS_API_KEY=your_newsapi_key
```

5. Run the application:
```bash
streamlit run app/app.py
```

## Usage

1. Open the application in your web browser (default: http://localhost:8501)
2. Choose your input method (text or webcam)
3. Get your emotion analysis
4. View personalized content recommendations
5. Save your mood and recommendations to your journal
6. Track your mood patterns over time

## Project Structure

```
moodboard-ai/
│
├── app/
│   ├── emotion/          # Emotion detection modules
│   ├── recommender/      # Content recommendation modules
│   ├── journal/          # Mood journaling functionality
│   ├── ui/              # UI components
│   ├── data/            # Data storage
│   └── utils/           # Utility functions
├── tests/               # Test files
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 