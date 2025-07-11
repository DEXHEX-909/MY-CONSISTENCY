#!/usr/bin/env python3
"""
Demo script for Audio Recorder & YouTube Uploader
This script demonstrates the core functionality without the GUI
"""

import time
import os
from datetime import datetime

from audio_recorder import AudioRecorder
from video_generator import VideoGenerator
from youtube_uploader import YouTubeUploader

def demo_recording():
    """Demo audio recording functionality"""
    print("🎤 Demo: Audio Recording")
    print("=" * 30)
    
    recorder = AudioRecorder()
    
    print("Starting 5-second recording...")
    print("Please speak into your microphone...")
    
    # Start recording
    recorder.is_recording = True
    stream = recorder.audio.open(
        format=recorder.format,
        channels=recorder.channels,
        rate=recorder.sample_rate,
        input=True,
        frames_per_buffer=recorder.chunk_size
    )
    
    # Record for 5 seconds
    start_time = time.time()
    while time.time() - start_time < 5:
        data = stream.read(recorder.chunk_size)
        recorder.frames.append(data)
    
    # Stop recording
    stream.stop_stream()
    stream.close()
    recorder.is_recording = False
    
    # Save audio
    audio_file = recorder.save_audio("demo_audio.wav")
    print(f"✅ Audio saved: {audio_file}")
    
    return audio_file

def demo_silence_removal(audio_file):
    """Demo silence removal functionality"""
    print("\n🔇 Demo: Silence Removal")
    print("=" * 30)
    
    recorder = AudioRecorder()
    
    if os.path.exists(audio_file):
        processed_file = recorder.remove_silence(audio_file, "demo_processed.wav")
        print(f"✅ Processed audio: {processed_file}")
        return processed_file
    else:
        print("❌ Audio file not found")
        return None

def demo_video_generation(audio_file):
    """Demo video generation functionality"""
    print("\n🎬 Demo: Video Generation")
    print("=" * 30)
    
    if not audio_file or not os.path.exists(audio_file):
        print("❌ No audio file available for video generation")
        return None
    
    generator = VideoGenerator()
    
    # Create different types of videos
    video_types = [
        ("Audio Visualizer", "demo_visualizer.mp4"),
        ("Waveform", "demo_waveform.mp4"),
        ("Circular Visualizer", "demo_circle.mp4"),
        ("Simple Background", "demo_simple.mp4")
    ]
    
    created_videos = []
    
    for video_type, filename in video_types:
        print(f"Creating {video_type}...")
        try:
            if video_type == "Audio Visualizer":
                video_file = generator.create_audio_visualizer(audio_file, filename)
            elif video_type == "Waveform":
                video_file = generator.create_waveform_video(audio_file, filename)
            elif video_type == "Circular Visualizer":
                video_file = generator.create_circle_visualizer(audio_file, filename)
            else:  # Simple Background
                video_file = generator.create_simple_background(audio_file, filename)
            
            if video_file and os.path.exists(video_file):
                created_videos.append(video_file)
                print(f"✅ {video_type}: {video_file}")
            else:
                print(f"❌ Failed to create {video_type}")
        except Exception as e:
            print(f"❌ Error creating {video_type}: {e}")
    
    return created_videos

def demo_youtube_setup():
    """Demo YouTube setup functionality"""
    print("\n📤 Demo: YouTube Setup")
    print("=" * 30)
    
    uploader = YouTubeUploader()
    
    # Create template file
    uploader.create_client_secrets_template()
    print("✅ Created client_secrets_template.json")
    print("📝 Please follow the instructions in the README to set up YouTube API")

def main():
    """Main demo function"""
    print("🎤 Audio Recorder & YouTube Uploader - Demo")
    print("=" * 50)
    
    # Check if we're in a suitable environment
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        
        if device_count == 0:
            print("⚠️ No audio devices found. Demo will skip recording.")
            print("Creating sample audio file for video generation...")
            
            # Create a simple test audio file
            import numpy as np
            import soundfile as sf
            
            # Generate a simple sine wave
            sample_rate = 44100
            duration = 3  # seconds
            frequency = 440  # Hz (A note)
            
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            audio = np.sin(2 * np.pi * frequency * t) * 0.3
            
            sf.write("demo_audio.wav", audio, sample_rate)
            audio_file = "demo_audio.wav"
            print("✅ Created test audio file")
        else:
            print(f"✅ Found {device_count} audio device(s)")
            audio_file = demo_recording()
    except Exception as e:
        print(f"⚠️ Audio setup error: {e}")
        print("Skipping recording demo...")
        audio_file = None
    
    # Demo silence removal
    if audio_file:
        processed_audio = demo_silence_removal(audio_file)
    else:
        processed_audio = audio_file
    
    # Demo video generation
    if processed_audio:
        videos = demo_video_generation(processed_audio)
    else:
        videos = demo_video_generation(audio_file)
    
    # Demo YouTube setup
    demo_youtube_setup()
    
    print("\n🎉 Demo completed!")
    print("=" * 50)
    print("📁 Generated files:")
    
    # List all generated files
    for filename in os.listdir('.'):
        if filename.startswith('demo_') and (filename.endswith('.wav') or filename.endswith('.mp4')):
            size = os.path.getsize(filename) / 1024  # KB
            print(f"   {filename} ({size:.1f} KB)")
    
    print("\n💡 To run the full application:")
    print("   python main_app.py")
    print("   or")
    print("   python run.py")

if __name__ == "__main__":
    main()