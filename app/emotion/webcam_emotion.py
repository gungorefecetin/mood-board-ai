import cv2
from fer import FER
import numpy as np
from typing import Optional, Dict, Any

class WebcamEmotionDetector:
    def __init__(self):
        """Initialize the FER emotion detector and webcam."""
        self.detector = FER(mtcnn=True)
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
    def get_emotion_from_frame(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Detect emotion from a single frame.
        
        Args:
            frame (np.ndarray): Input frame from webcam
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary containing emotion data or None if no face detected
        """
        # Convert frame to RGB (FER expects RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect emotions
        result = self.detector.detect_emotions(rgb_frame)
        
        if not result:  # No face detected
            return None
            
        # Get the first face detected (assuming single user)
        face_data = result[0]
        emotions = face_data['emotions']
        
        # Get the dominant emotion
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        
        return {
            'primary_emotion': dominant_emotion[0],
            'confidence': dominant_emotion[1],
            'all_emotions': emotions,
            'face_box': face_data['box']
        }
    
    def process_webcam(self, frame: np.ndarray) -> tuple:
        """
        Process webcam frame and draw emotion data.
        
        Args:
            frame (np.ndarray): Input frame from webcam
            
        Returns:
            tuple: (processed_frame, emotion_data)
        """
        # Make a copy of the frame to draw on
        display_frame = frame.copy()
        
        # Get emotion data
        emotion_data = self.get_emotion_from_frame(frame)
        
        if emotion_data:
            # Get face box coordinates
            x, y, w, h = emotion_data['face_box']
            
            # Draw face box
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Draw emotion label
            emotion = emotion_data['primary_emotion']
            confidence = emotion_data['confidence']
            label = f"{emotion}: {confidence:.2f}"
            cv2.putText(display_frame, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        return display_frame, emotion_data 