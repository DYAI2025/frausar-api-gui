"""
Enhanced Wake Word Detection with Multiple Trigger Words and Auto-Listen Mode
Supports: THOR, THORA, DORA, DOR, TOR, ORA + Auto-Listen after inactivity
"""

import threading
import time
import speech_recognition as sr
from typing import Callable, Optional, List, Set
from loguru import logger
import difflib


class EnhancedWakeWordDetector:
    """Enhanced Wake Word Detector with multiple trigger words and auto-listen mode"""
    
    def __init__(self, on_wake_callback: Callable[[], None], 
                 wake_words: Optional[List[str]] = None,
                 auto_listen_timeout: int = 120,  # 2 minutes
                 similarity_threshold: float = 0.7):
        """
        Initialize Enhanced Wake Word Detector
        
        Args:
            on_wake_callback: Function to call when wake word detected
            wake_words: List of wake words (default: THOR variants)
            auto_listen_timeout: Seconds of inactivity before auto-listen mode
            similarity_threshold: Minimum similarity for fuzzy matching (0.0-1.0)
        """
        self.on_wake_callback = on_wake_callback
        self.wake_words = wake_words or ["THOR", "THORA", "DORA", "DOR", "TOR", "ORA"]
        self.auto_listen_timeout = auto_listen_timeout
        self.similarity_threshold = similarity_threshold
        
        # State management
        self.is_running = False
        self.is_listening_mode = False
        self.last_interaction_time = time.time()
        
        # Speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Threading
        self.listen_thread: Optional[threading.Thread] = None
        self.auto_listen_thread: Optional[threading.Thread] = None
        
        # Adjust microphone for ambient noise
        self._calibrate_microphone()
        
        logger.info(f"Enhanced Wake Word Detector initialized with words: {self.wake_words}")
        
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            logger.info("Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("✅ Microphone calibrated successfully")
        except Exception as e:
            logger.warning(f"Microphone calibration failed: {e}")
            
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison"""
        return text.upper().strip().replace(".", "").replace(",", "").replace("!", "").replace("?", "")
        
    def _is_wake_word_detected(self, text: str) -> bool:
        """Check if text contains any wake word with fuzzy matching"""
        normalized_text = self._normalize_text(text)
        words_in_text = normalized_text.split()
        
        # Direct word matching
        for word in words_in_text:
            if word in self.wake_words:
                logger.info(f"🎯 Direct wake word match: '{word}'")
                return True
                
        # Fuzzy matching for each word in the text
        for word in words_in_text:
            for wake_word in self.wake_words:
                similarity = difflib.SequenceMatcher(None, word, wake_word).ratio()
                if similarity >= self.similarity_threshold:
                    logger.info(f"🎯 Fuzzy wake word match: '{word}' ~ '{wake_word}' (similarity: {similarity:.2f})")
                    return True
                    
        return False
        
    def _listen_continuously(self):
        """Main listening loop for wake word detection"""
        logger.info("🎤 Starting continuous wake word listening...")
        
        while self.is_running:
            try:
                # Listen for audio with timeout
                with self.microphone as source:
                    # Short timeout to allow for regular checks
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                try:
                    # Recognize speech with German language
                    text = self.recognizer.recognize_google(audio, language="de-DE")
                    logger.debug(f"🎧 Heard: '{text}'")
                    
                    # Check for wake words
                    if self._is_wake_word_detected(text):
                        logger.info(f"⚡ Wake word detected in: '{text}'")
                        self.update_last_interaction()
                        self.on_wake_callback()
                        
                    # In listening mode, treat any speech as activation
                    elif self.is_listening_mode and text.strip():
                        logger.info(f"👂 Listening mode: responding to speech: '{text}'")
                        self.update_last_interaction()
                        self.on_wake_callback()
                        
                except sr.UnknownValueError:
                    # No speech detected, continue listening
                    pass
                except sr.RequestError as e:
                    logger.error(f"Speech recognition service error: {e}")
                    time.sleep(1)  # Wait before retrying
                    
            except sr.WaitTimeoutError:
                # Timeout reached, continue loop
                pass
            except Exception as e:
                logger.error(f"Error in listening loop: {e}")
                time.sleep(1)  # Wait before retrying
                
        logger.info("🛑 Wake word listening stopped")
        
    def _auto_listen_monitor(self):
        """Monitor for auto-listen activation after inactivity"""
        logger.info(f"⏰ Auto-listen monitor started (timeout: {self.auto_listen_timeout}s)")
        
        while self.is_running:
            try:
                time.sleep(10)  # Check every 10 seconds
                
                if not self.is_running:
                    break
                    
                # Check if enough time has passed since last interaction
                time_since_interaction = time.time() - self.last_interaction_time
                
                if time_since_interaction >= self.auto_listen_timeout and not self.is_listening_mode:
                    logger.info(f"⏰ Auto-activating listening mode after {time_since_interaction:.1f}s of inactivity")
                    self.enter_listening_mode()
                    
            except Exception as e:
                logger.error(f"Error in auto-listen monitor: {e}")
                time.sleep(5)
                
        logger.info("🛑 Auto-listen monitor stopped")
        
    def start(self):
        """Start wake word detection"""
        if self.is_running:
            logger.warning("Wake word detector already running")
            return
            
        self.is_running = True
        self.update_last_interaction()
        
        # Start listening thread
        self.listen_thread = threading.Thread(target=self._listen_continuously, daemon=True)
        self.listen_thread.start()
        
        # Start auto-listen monitor thread
        self.auto_listen_thread = threading.Thread(target=self._auto_listen_monitor, daemon=True)
        self.auto_listen_thread.start()
        
        logger.info("🚀 Enhanced Wake Word Detector started")
        
    def stop(self):
        """Stop wake word detection"""
        if not self.is_running:
            return
            
        logger.info("Stopping Enhanced Wake Word Detector...")
        self.is_running = False
        self.is_listening_mode = False
        
        # Wait for threads to finish
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2)
            
        if self.auto_listen_thread and self.auto_listen_thread.is_alive():
            self.auto_listen_thread.join(timeout=2)
            
        logger.info("✅ Enhanced Wake Word Detector stopped")
        
    def update_last_interaction(self):
        """Update the timestamp of last interaction"""
        self.last_interaction_time = time.time()
        
        # Exit listening mode if we were in it
        if self.is_listening_mode:
            self.exit_listening_mode()
            
    def enter_listening_mode(self):
        """Enter continuous listening mode"""
        if not self.is_listening_mode:
            self.is_listening_mode = True
            logger.info("👂 Entered listening mode - responding to any speech")
            
    def exit_listening_mode(self):
        """Exit continuous listening mode"""
        if self.is_listening_mode:
            self.is_listening_mode = False
            logger.info("🔇 Exited listening mode - back to wake word detection")
            
    def get_status(self) -> dict:
        """Get current detector status"""
        return {
            "is_running": self.is_running,
            "is_listening_mode": self.is_listening_mode,
            "wake_words": self.wake_words,
            "last_interaction": self.last_interaction_time,
            "time_since_interaction": time.time() - self.last_interaction_time,
            "auto_listen_timeout": self.auto_listen_timeout
        }


class MockEnhancedWakeWordDetector:
    """Mock Enhanced Wake Word Detector for testing"""
    
    def __init__(self, on_wake_callback: Callable[[], None], **kwargs):
        self.on_wake_callback = on_wake_callback
        self.is_running = False
        self.is_listening_mode = False
        self.last_interaction_time = time.time()
        logger.info("🧪 Mock Enhanced Wake Word Detector initialized")
        
    def start(self):
        """Start mock detector"""
        self.is_running = True
        logger.info("🧪 Mock Enhanced Wake Word Detector started (press Enter to simulate wake word)")
        
        # Start a thread that waits for Enter key
        def wait_for_enter():
            while self.is_running:
                try:
                    input()  # Wait for Enter key
                    if self.is_running:
                        logger.info("🧪 Mock wake word detected!")
                        self.update_last_interaction()
                        self.on_wake_callback()
                except EOFError:
                    break
                except KeyboardInterrupt:
                    break
                    
        import threading
        self.mock_thread = threading.Thread(target=wait_for_enter, daemon=True)
        self.mock_thread.start()
        
    def stop(self):
        """Stop mock detector"""
        self.is_running = False
        logger.info("🧪 Mock Enhanced Wake Word Detector stopped")
        
    def update_last_interaction(self):
        """Update interaction timestamp"""
        self.last_interaction_time = time.time()
        if self.is_listening_mode:
            self.exit_listening_mode()
            
    def enter_listening_mode(self):
        """Enter mock listening mode"""
        self.is_listening_mode = True
        logger.info("🧪 Mock: Entered listening mode")
        
    def exit_listening_mode(self):
        """Exit mock listening mode"""
        self.is_listening_mode = False
        logger.info("🧪 Mock: Exited listening mode")
        
    def get_status(self) -> dict:
        """Get mock status"""
        return {
            "is_running": self.is_running,
            "is_listening_mode": self.is_listening_mode,
            "wake_words": ["MOCK"],
            "last_interaction": self.last_interaction_time,
            "time_since_interaction": time.time() - self.last_interaction_time,
            "auto_listen_timeout": 120,
            "mock_mode": True
        }


if __name__ == "__main__":
    """Test the Enhanced Wake Word Detector"""
    
    def test_callback():
        print("🎯 Wake word detected!")
        
    # Test with mock detector
    detector = MockEnhancedWakeWordDetector(test_callback)
    
    try:
        detector.start()
        print("Press Enter to simulate wake word detection, Ctrl+C to exit")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        detector.stop()
        print("\nTest completed") 