import pytest
from app.emotion.text_emotion import TextEmotionDetector
import numpy as np

def test_text_emotion_detector():
    detector = TextEmotionDetector()
    
    # Test happy text
    result = detector.get_emotion("I'm feeling really happy and excited today!")
    assert isinstance(result, dict)
    assert 'primary_emotion' in result
    assert 'confidence' in result
    assert isinstance(result['confidence'], float)
    assert 0 <= result['confidence'] <= 1
    
    # Test sad text
    result = detector.get_emotion("I'm feeling very sad and depressed.")
    assert isinstance(result, dict)
    assert 'primary_emotion' in result
    assert 'confidence' in result
    
    # Test empty text
    result = detector.get_emotion("")
    assert isinstance(result, dict)
    assert 'primary_emotion' in result
    
def test_emotion_confidence():
    detector = TextEmotionDetector()
    result = detector.get_emotion("I'm feeling great!")
    assert 'confidence' in result
    assert isinstance(result['confidence'], float)
    assert 0 <= result['confidence'] <= 1

def test_emotion_categories():
    detector = TextEmotionDetector()
    valid_emotions = {'happy', 'sad', 'angry', 'fear', 'surprise', 'disgust', 'neutral'}
    
    test_texts = [
        "I'm so happy!",
        "I'm feeling sad",
        "I'm really angry",
        "I'm scared",
        "Wow, that's surprising!",
        "That's disgusting",
        "Just a normal day"
    ]
    
    for text in test_texts:
        result = detector.get_emotion(text)
        assert result['primary_emotion'].lower() in valid_emotions 