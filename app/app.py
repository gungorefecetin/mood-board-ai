import streamlit as st
import cv2
import numpy as np
from PIL import Image
from emotion.text_emotion import TextEmotionDetector
from emotion.webcam_emotion import WebcamEmotionDetector
from recommender.music import SpotifyRecommender
from recommender.movies import MovieRecommender
from recommender.quotes import QuoteRecommender
from journal.journal import MoodJournal
import plotly.graph_objects as go
from datetime import datetime

# Initialize components
text_detector = TextEmotionDetector()
webcam_detector = WebcamEmotionDetector()
music_recommender = SpotifyRecommender()
movie_recommender = MovieRecommender()
quote_recommender = QuoteRecommender()
journal = MoodJournal()

# Page config
st.set_page_config(
    page_title="MoodBoard AI",
    page_icon="🎭",
    layout="wide"
)

# Title and description
st.title("🎭 MoodBoard AI")
st.markdown("""
Discover content that matches your mood! Share how you're feeling through text or webcam,
and get personalized recommendations for music, movies, and inspirational quotes.
""")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Mood Detection", "Journal & Analytics"])

if page == "Mood Detection":
    # Input method selection
    input_method = st.radio("Choose input method:", ["Text", "Webcam"])
    
    detected_emotion = None
    confidence = None
    
    if input_method == "Text":
        # Text input
        text_input = st.text_area("How are you feeling? (Describe your mood)")
        if text_input and st.button("Analyze"):
            with st.spinner("Analyzing your mood..."):
                result = text_detector.get_emotion(text_input)
                detected_emotion = result['primary_emotion']
                confidence = result['confidence']
                
    else:
        # Webcam input
        st.warning("Note: Webcam access is required for this feature")
        if st.button("Start Webcam"):
            picture = st.camera_input("Take a picture")
            
            if picture:
                # Convert to CV2 format
                file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
                frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                
                # Process frame
                with st.spinner("Analyzing your expression..."):
                    processed_frame, emotion_data = webcam_detector.process_webcam(frame)
                    if emotion_data:
                        detected_emotion = emotion_data['primary_emotion']
                        confidence = emotion_data['confidence']
                        
                        # Display processed frame
                        st.image(processed_frame, channels="BGR")
    
    # Display results and recommendations
    if detected_emotion and confidence:
        # Create columns for recommendations
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"Detected Emotion: {detected_emotion.title()} (Confidence: {confidence:.2f})")
            
            # Music recommendations
            st.subheader("🎵 Music Recommendations")
            with st.spinner("Getting music recommendations..."):
                songs = music_recommender.get_recommendations(detected_emotion)
                for song in songs:
                    st.write(f"**{song['name']}** by {song['artist']}")
                    if song['preview_url']:
                        st.audio(song['preview_url'])
                    if song['album_image']:
                        st.image(song['album_image'], width=100)
                    st.markdown(f"[Listen on Spotify]({song['external_url']})")
            
            # Quotes
            st.subheader("💭 Inspirational Quotes")
            with st.spinner("Finding relevant quotes..."):
                quotes = quote_recommender.get_recommendations(detected_emotion)
                for quote in quotes:
                    st.markdown(f"> {quote['content']}")
                    st.markdown(f"— *{quote['author']}*")
        
        with col2:
            # Movie recommendations
            st.subheader("🎬 Movie Recommendations")
            with st.spinner("Getting movie recommendations..."):
                movies = movie_recommender.get_recommendations(detected_emotion)
                for movie in movies:
                    st.markdown(f"### {movie['title']} ({movie['release_date'][:4]})")
                    if movie['poster_path']:
                        st.image(movie['poster_path'], width=200)
                    st.markdown(f"**Rating:** ⭐ {movie['rating']}/10")
                    st.markdown(f"**Runtime:** {movie['runtime']} minutes")
                    st.markdown(f"**Genres:** {', '.join(movie['genres'])}")
                    with st.expander("Overview"):
                        st.write(movie['overview'])
                    st.markdown(f"[View on TMDB]({movie['tmdb_url']})")
        
        # Save to journal
        if st.button("Save to Journal"):
            recommendations = {
                'music': songs,
                'movies': movies,
                'quotes': quotes
            }
            journal.add_entry(
                emotion=detected_emotion,
                confidence=confidence,
                input_text=text_input if input_method == "Text" else None,
                recommendations=recommendations
            )
            st.success("Saved to your mood journal!")

else:  # Journal & Analytics page
    st.header("📊 Mood Journal & Analytics")
    
    # Get journal data
    entries = journal.load_entries()
    
    if not entries:
        st.info("Your mood journal is empty. Start by analyzing your mood!")
    else:
        # Display analytics
        st.subheader("Mood Analytics")
        
        # Create visualizations
        viz_data = journal.create_visualization()
        if viz_data:
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(go.Figure(viz_data['distribution']))
            
            with col2:
                st.plotly_chart(go.Figure(viz_data['timeline']))
        
        # Display recent entries
        st.subheader("Recent Entries")
        for entry in reversed(entries[-5:]):  # Show last 5 entries
            with st.expander(f"{entry['emotion'].title()} - {entry['timestamp']}"):
                st.write(f"**Confidence:** {entry['confidence']:.2f}")
                if entry['input_text']:
                    st.write(f"**Input:** {entry['input_text']}")
                
                if entry['recommendations']:
                    st.write("**Recommendations:**")
                    if 'music' in entry['recommendations']:
                        st.write("🎵 Music:", ", ".join(song['name'] for song in entry['recommendations']['music'][:3]))
                    if 'movies' in entry['recommendations']:
                        st.write("🎬 Movies:", ", ".join(movie['title'] for movie in entry['recommendations']['movies'][:3]))
                    if 'quotes' in entry['recommendations']:
                        st.write("💭 Quote:", entry['recommendations']['quotes'][0]['content']) 