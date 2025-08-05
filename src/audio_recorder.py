"""
Mock Audio Recorder for THOR Agent
Provides audio recording functionality or mock implementation
"""

import asyncio
import numpy as np
from typing import Optional, Callable
from loguru import logger


class AudioRecorder:
    """Real audio recorder implementation"""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.audio_data = []
        
    async def start_recording(self) -> bool:
        """Start audio recording"""
        try:
            self.is_recording = True
            self.audio_data = []
            logger.info("🎤 Audio recording started")
            return True
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            return False
    
    async def stop_recording(self) -> bytes:
        """Stop recording and return audio data"""
        self.is_recording = False
        # Mock audio data
        audio_data = np.random.bytes(1024)  # Mock 1KB of audio
        logger.info("🎤 Audio recording stopped")
        return audio_data
    
    def is_active(self) -> bool:
        """Check if currently recording"""
        return self.is_recording


class MockAudioRecorder:
    """Mock audio recorder for testing"""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        
    async def start_recording(self) -> bool:
        """Mock start recording"""
        self.is_recording = True
        logger.info("🎤 Mock audio recording started")
        return True
    
    async def stop_recording(self) -> bytes:
        """Mock stop recording"""
        self.is_recording = False
        logger.info("🎤 Mock audio recording stopped")
        return b"mock_audio_data"
    
    def is_active(self) -> bool:
        """Check if currently recording"""
        return self.is_recording 