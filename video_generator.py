import numpy as np
import cv2
import librosa
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, ColorClip
from moviepy.video.fx import resize
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import os

class VideoGenerator:
    def __init__(self, width=1920, height=1080, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        
    def create_audio_visualizer(self, audio_file, output_file="video_with_visualizer.mp4"):
        """Create a video with audio visualizer"""
        print("🎨 Creating audio visualizer...")
        
        # Load audio
        y, sr = librosa.load(audio_file, sr=44100)
        duration = len(y) / sr
        
        # Create spectrogram
        D = librosa.stft(y)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        
        # Create video frames
        frames = []
        frame_duration = 1.0 / self.fps
        samples_per_frame = int(sr * frame_duration)
        
        for i in range(int(duration * self.fps)):
            start_sample = i * samples_per_frame
            end_sample = min(start_sample + samples_per_frame, len(y))
            
            if start_sample >= len(y):
                break
                
            # Get frequency data for this frame
            frame_start = start_sample // 512  # hop length
            frame_end = min(frame_start + 1, S_db.shape[1])
            
            if frame_start < S_db.shape[1]:
                frequencies = S_db[:, frame_start]
            else:
                frequencies = np.zeros(S_db.shape[0])
            
            # Create visualizer frame
            frame = self.create_visualizer_frame(frequencies)
            frames.append(frame)
        
        # Create video from frames
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, self.fps, (self.width, self.height))
        
        for frame in frames:
            out.write(frame)
        
        out.release()
        
        # Add audio to video
        self.add_audio_to_video(output_file, audio_file, output_file)
        
        print(f"✅ Video with visualizer created: {output_file}")
        return output_file
    
    def create_visualizer_frame(self, frequencies):
        """Create a single visualizer frame"""
        # Create black background
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Normalize frequencies
        if len(frequencies) > 0:
            frequencies = np.abs(frequencies)
            frequencies = (frequencies - np.min(frequencies)) / (np.max(frequencies) - np.min(frequencies) + 1e-8)
        
        # Create bars
        num_bars = 100
        bar_width = self.width // num_bars
        
        for i in range(num_bars):
            if i < len(frequencies):
                height = int(frequencies[i] * self.height * 0.8)
            else:
                height = 0
            
            # Create gradient color based on frequency
            hue = int((i / num_bars) * 180)  # 0-180 for OpenCV
            color = cv2.cvtColor(np.uint8([[[hue, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
            
            # Draw bar
            x = i * bar_width
            y = self.height - height
            cv2.rectangle(frame, (x, y), (x + bar_width - 2, self.height), color.tolist(), -1)
        
        return frame
    
    def create_simple_background(self, audio_file, output_file="video_simple.mp4", background_color=(0, 0, 0)):
        """Create a simple video with static background"""
        print("🎬 Creating simple video with static background...")
        
        # Load audio
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        
        # Create color background
        background = ColorClip(size=(self.width, self.height), color=background_color, duration=duration)
        
        # Combine audio and video
        final_video = background.set_audio(audio_clip)
        final_video.write_videofile(output_file, fps=self.fps, codec='libx264', audio_codec='aac')
        
        print(f"✅ Simple video created: {output_file}")
        return output_file
    
    def create_waveform_video(self, audio_file, output_file="video_waveform.mp4"):
        """Create a video with waveform visualization"""
        print("🌊 Creating waveform video...")
        
        # Load audio
        y, sr = librosa.load(audio_file, sr=44100)
        duration = len(y) / sr
        
        # Create video frames
        frames = []
        frame_duration = 1.0 / self.fps
        samples_per_frame = int(sr * frame_duration)
        
        for i in range(int(duration * self.fps)):
            start_sample = i * samples_per_frame
            end_sample = min(start_sample + samples_per_frame, len(y))
            
            if start_sample >= len(y):
                break
            
            # Get audio segment for this frame
            frame_audio = y[start_sample:end_sample]
            
            # Create waveform frame
            frame = self.create_waveform_frame(frame_audio)
            frames.append(frame)
        
        # Create video from frames
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, self.fps, (self.width, self.height))
        
        for frame in frames:
            out.write(frame)
        
        out.release()
        
        # Add audio to video
        self.add_audio_to_video(output_file, audio_file, output_file)
        
        print(f"✅ Waveform video created: {output_file}")
        return output_file
    
    def create_waveform_frame(self, audio_segment):
        """Create a single waveform frame"""
        # Create black background
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        if len(audio_segment) == 0:
            return frame
        
        # Resample audio to fit width
        audio_resampled = np.interp(
            np.linspace(0, len(audio_segment), self.width),
            np.arange(len(audio_segment)),
            audio_segment
        )
        
        # Draw waveform
        center_y = self.height // 2
        
        for x in range(self.width):
            if x < len(audio_resampled):
                amplitude = audio_resampled[x]
                height = int(abs(amplitude) * self.height * 0.3)
                
                # Create gradient color
                intensity = min(255, int(abs(amplitude) * 255))
                color = (intensity, intensity, 255)  # Blue gradient
                
                # Draw line
                y1 = center_y - height
                y2 = center_y + height
                cv2.line(frame, (x, y1), (x, y2), color, 1)
        
        return frame
    
    def add_audio_to_video(self, video_file, audio_file, output_file):
        """Add audio to video file"""
        try:
            video = VideoFileClip(video_file)
            audio = AudioFileClip(audio_file)
            
            # Set audio to video
            final_video = video.set_audio(audio)
            final_video.write_videofile(output_file, fps=self.fps, codec='libx264', audio_codec='aac')
            
            video.close()
            audio.close()
            final_video.close()
            
        except Exception as e:
            print(f"⚠️ Warning: Could not add audio to video: {e}")
            # If adding audio fails, just copy the video
            import shutil
            shutil.copy2(video_file, output_file)
    
    def create_circle_visualizer(self, audio_file, output_file="video_circle.mp4"):
        """Create a circular audio visualizer"""
        print("⭕ Creating circular visualizer...")
        
        # Load audio
        y, sr = librosa.load(audio_file, sr=44100)
        duration = len(y) / sr
        
        # Create video frames
        frames = []
        frame_duration = 1.0 / self.fps
        samples_per_frame = int(sr * frame_duration)
        
        for i in range(int(duration * self.fps)):
            start_sample = i * samples_per_frame
            end_sample = min(start_sample + samples_per_frame, len(y))
            
            if start_sample >= len(y):
                break
            
            # Get audio segment for this frame
            frame_audio = y[start_sample:end_sample]
            
            # Create circular frame
            frame = self.create_circle_frame(frame_audio)
            frames.append(frame)
        
        # Create video from frames
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, self.fps, (self.width, self.height))
        
        for frame in frames:
            out.write(frame)
        
        out.release()
        
        # Add audio to video
        self.add_audio_to_video(output_file, audio_file, output_file)
        
        print(f"✅ Circular visualizer created: {output_file}")
        return output_file
    
    def create_circle_frame(self, audio_segment):
        """Create a single circular visualizer frame"""
        # Create black background
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        if len(audio_segment) == 0:
            return frame
        
        # Calculate RMS for this frame
        rms = np.sqrt(np.mean(audio_segment**2))
        
        # Create circular visualization
        center_x, center_y = self.width // 2, self.height // 2
        max_radius = min(self.width, self.height) // 3
        
        # Draw multiple circles with different intensities
        for radius in range(0, max_radius, 10):
            intensity = int(min(255, rms * 255 * (1 - radius / max_radius)))
            color = (intensity, intensity, 255)  # Blue gradient
            
            cv2.circle(frame, (center_x, center_y), radius, color, 2)
        
        return frame