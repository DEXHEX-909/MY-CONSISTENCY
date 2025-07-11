import pyaudio
import numpy as np
import wave
import threading
import time
import librosa
import soundfile as sf
from scipy.signal import find_peaks
import os

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.sample_rate = 44100
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paFloat32
        
    def start_recording(self):
        """Start recording audio"""
        self.frames = []
        self.is_recording = True
        
        stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        print("🎤 Recording started... Press Ctrl+. to stop")
        
        while self.is_recording:
            try:
                data = stream.read(self.chunk_size)
                self.frames.append(data)
            except KeyboardInterrupt:
                break
        
        stream.stop_stream()
        stream.close()
        
        return self.save_audio()
    
    def stop_recording(self):
        """Stop recording audio"""
        self.is_recording = False
        print("⏹️ Recording stopped")
    
    def save_audio(self, filename="raw_audio.wav"):
        """Save recorded audio to file"""
        if not self.frames:
            return None
            
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
        
        print(f"💾 Audio saved as {filename}")
        return filename
    
    def remove_silence(self, input_file, output_file="processed_audio.wav", 
                      silence_threshold=-40, min_silence_duration=0.5):
        """Remove silence from audio file"""
        print("🔇 Removing silence...")
        
        # Load audio
        y, sr = librosa.load(input_file, sr=self.sample_rate)
        
        # Convert to dB
        db = librosa.amplitude_to_db(np.abs(y), ref=np.max)
        
        # Find non-silent regions
        non_silent_mask = db > silence_threshold
        
        # Find silence regions
        silence_regions = []
        start = None
        
        for i, is_silent in enumerate(non_silent_mask):
            if not is_silent and start is None:
                start = i
            elif is_silent and start is not None:
                silence_regions.append((start, i))
                start = None
        
        if start is not None:
            silence_regions.append((start, len(non_silent_mask)))
        
        # Remove short silences
        min_silence_samples = int(min_silence_duration * sr)
        filtered_regions = []
        
        for start, end in silence_regions:
            if end - start >= min_silence_samples:
                filtered_regions.append((start, end))
        
        # Create new audio without silence
        if filtered_regions:
            # Keep only non-silent regions
            final_audio = np.array([])
            for start, end in filtered_regions:
                final_audio = np.concatenate([final_audio, y[start:end]])
        else:
            final_audio = y
        
        # Save processed audio
        sf.write(output_file, final_audio, sr)
        print(f"✅ Silence removed! Processed audio saved as {output_file}")
        
        return output_file
    
    def get_audio_duration(self, filename):
        """Get duration of audio file"""
        y, sr = librosa.load(filename, sr=self.sample_rate)
        return len(y) / sr
    
    def cleanup(self):
        """Clean up resources"""
        self.audio.terminate()