import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import keyboard
import time
import os
from datetime import datetime
import json

from audio_recorder import AudioRecorder
from video_generator import VideoGenerator
from youtube_uploader import YouTubeUploader

class AudioVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Audio Recorder & YouTube Uploader")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize components
        self.audio_recorder = AudioRecorder()
        self.video_generator = VideoGenerator()
        self.youtube_uploader = YouTubeUploader()
        
        # State variables
        self.is_recording = False
        self.recording_thread = None
        self.current_audio_file = None
        self.current_video_file = None
        
        # Load settings
        self.settings = self.load_settings()
        
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🎤 Audio Recorder & YouTube Uploader", 
            font=("Arial", 20, "bold"),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        title_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = tk.LabelFrame(
            main_frame, 
            text="Status", 
            bg='#2b2b2b', 
            fg='#ffffff',
            font=("Arial", 12, "bold")
        )
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to record (Press Ctrl+. to start/stop)",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        self.status_label.pack(pady=10)
        
        # Recording controls
        controls_frame = tk.LabelFrame(
            main_frame,
            text="Recording Controls",
            bg='#2b2b2b',
            fg='#ffffff',
            font=("Arial", 12, "bold")
        )
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(controls_frame, bg='#2b2b2b')
        buttons_frame.pack(pady=10)
        
        self.record_button = tk.Button(
            buttons_frame,
            text="🎤 Start Recording",
            command=self.toggle_recording,
            font=("Arial", 12, "bold"),
            bg='#ff4444',
            fg='white',
            width=15,
            height=2
        )
        self.record_button.pack(side=tk.LEFT, padx=5)
        
        # Video generation frame
        video_frame = tk.LabelFrame(
            main_frame,
            text="Video Generation",
            bg='#2b2b2b',
            fg='#ffffff',
            font=("Arial", 12, "bold")
        )
        video_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Video type selection
        video_type_frame = tk.Frame(video_frame, bg='#2b2b2b')
        video_type_frame.pack(pady=10)
        
        tk.Label(
            video_type_frame,
            text="Video Type:",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#ffffff'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.video_type = tk.StringVar(value="visualizer")
        video_types = [
            ("Audio Visualizer", "visualizer"),
            ("Waveform", "waveform"),
            ("Circular Visualizer", "circle"),
            ("Simple Black Background", "simple")
        ]
        
        for text, value in video_types:
            tk.Radiobutton(
                video_type_frame,
                text=text,
                variable=self.video_type,
                value=value,
                bg='#2b2b2b',
                fg='#ffffff',
                selectcolor='#2b2b2b',
                font=("Arial", 10)
            ).pack(side=tk.LEFT, padx=5)
        
        # Generate video button
        self.generate_button = tk.Button(
            video_frame,
            text="🎬 Generate Video",
            command=self.generate_video,
            font=("Arial", 12, "bold"),
            bg='#4444ff',
            fg='white',
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.generate_button.pack(pady=10)
        
        # YouTube upload frame
        youtube_frame = tk.LabelFrame(
            main_frame,
            text="YouTube Upload",
            bg='#2b2b2b',
            fg='#ffffff',
            font=("Arial", 12, "bold")
        )
        youtube_frame.pack(fill=tk.X, pady=(0, 20))
        
        # YouTube settings
        youtube_settings_frame = tk.Frame(youtube_frame, bg='#2b2b2b')
        youtube_settings_frame.pack(pady=10, fill=tk.X)
        
        # Title
        tk.Label(
            youtube_settings_frame,
            text="Title:",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#ffffff'
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.title_entry = tk.Entry(
            youtube_settings_frame,
            font=("Arial", 10),
            width=40
        )
        self.title_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        self.title_entry.insert(0, "My Audio Recording")
        
        # Description
        tk.Label(
            youtube_settings_frame,
            text="Description:",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#ffffff'
        ).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        self.description_text = tk.Text(
            youtube_settings_frame,
            height=3,
            width=40,
            font=("Arial", 10)
        )
        self.description_text.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=(10, 0))
        
        # Privacy
        tk.Label(
            youtube_settings_frame,
            text="Privacy:",
            font=("Arial", 10),
            bg='#2b2b2b',
            fg='#ffffff'
        ).grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        self.privacy_var = tk.StringVar(value="private")
        privacy_frame = tk.Frame(youtube_settings_frame, bg='#2b2b2b')
        privacy_frame.grid(row=2, column=1, sticky=tk.W, padx=(0, 20), pady=(10, 0))
        
        tk.Radiobutton(
            privacy_frame,
            text="Private",
            variable=self.privacy_var,
            value="private",
            bg='#2b2b2b',
            fg='#ffffff',
            selectcolor='#2b2b2b',
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Radiobutton(
            privacy_frame,
            text="Unlisted",
            variable=self.privacy_var,
            value="unlisted",
            bg='#2b2b2b',
            fg='#ffffff',
            selectcolor='#2b2b2b',
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Radiobutton(
            privacy_frame,
            text="Public",
            variable=self.privacy_var,
            value="public",
            bg='#2b2b2b',
            fg='#ffffff',
            selectcolor='#2b2b2b',
            font=("Arial", 10)
        ).pack(side=tk.LEFT)
        
        # Upload button
        self.upload_button = tk.Button(
            youtube_frame,
            text="📤 Upload to YouTube",
            command=self.upload_to_youtube,
            font=("Arial", 12, "bold"),
            bg='#ff8800',
            fg='white',
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.upload_button.pack(pady=10)
        
        # Settings button
        settings_button = tk.Button(
            main_frame,
            text="⚙️ YouTube Setup",
            command=self.show_youtube_setup,
            font=("Arial", 10),
            bg='#666666',
            fg='white',
            width=15
        )
        settings_button.pack(pady=(20, 0))
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        try:
            keyboard.add_hotkey('ctrl+.', self.toggle_recording)
            print("⌨️ Keyboard shortcut Ctrl+. registered")
        except Exception as e:
            print(f"⚠️ Could not register keyboard shortcut: {e}")
    
    def toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Start recording audio"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.status_label.config(text="🎤 Recording... Press Ctrl+. to stop", fg='#ff4444')
        self.record_button.config(text="⏹️ Stop Recording", bg='#ff8800')
        
        # Start recording in separate thread
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.daemon = True
        self.recording_thread.start()
    
    def stop_recording(self):
        """Stop recording audio"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        self.audio_recorder.stop_recording()
        
        self.status_label.config(text="⏹️ Recording stopped. Processing audio...", fg='#ff8800')
        self.record_button.config(text="🎤 Start Recording", bg='#ff4444')
        
        # Process audio in separate thread
        processing_thread = threading.Thread(target=self.process_audio)
        processing_thread.daemon = True
        processing_thread.start()
    
    def record_audio(self):
        """Record audio in separate thread"""
        try:
            self.current_audio_file = self.audio_recorder.start_recording()
        except Exception as e:
            print(f"❌ Recording error: {e}")
            self.root.after(0, lambda: self.status_label.config(
                text=f"❌ Recording error: {e}", fg='#ff4444'))
    
    def process_audio(self):
        """Process recorded audio"""
        try:
            if self.current_audio_file and os.path.exists(self.current_audio_file):
                # Remove silence
                processed_audio = self.audio_recorder.remove_silence(self.current_audio_file)
                
                if processed_audio:
                    self.current_audio_file = processed_audio
                    self.root.after(0, lambda: self.status_label.config(
                        text="✅ Audio processed! Ready to generate video.", fg='#00ff00'))
                    self.root.after(0, lambda: self.generate_button.config(state=tk.NORMAL))
                else:
                    self.root.after(0, lambda: self.status_label.config(
                        text="❌ Failed to process audio", fg='#ff4444'))
            else:
                self.root.after(0, lambda: self.status_label.config(
                    text="❌ No audio file found", fg='#ff4444'))
        except Exception as e:
            print(f"❌ Processing error: {e}")
            self.root.after(0, lambda: self.status_label.config(
                text=f"❌ Processing error: {e}", fg='#ff4444'))
    
    def generate_video(self):
        """Generate video from audio"""
        if not self.current_audio_file or not os.path.exists(self.current_audio_file):
            messagebox.showerror("Error", "No audio file available!")
            return
        
        self.status_label.config(text="🎬 Generating video...", fg='#ff8800')
        self.generate_button.config(state=tk.DISABLED)
        
        # Generate video in separate thread
        video_thread = threading.Thread(target=self.generate_video_thread)
        video_thread.daemon = True
        video_thread.start()
    
    def generate_video_thread(self):
        """Generate video in separate thread"""
        try:
            video_type = self.video_type.get()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if video_type == "visualizer":
                output_file = f"video_visualizer_{timestamp}.mp4"
                self.current_video_file = self.video_generator.create_audio_visualizer(
                    self.current_audio_file, output_file)
            elif video_type == "waveform":
                output_file = f"video_waveform_{timestamp}.mp4"
                self.current_video_file = self.video_generator.create_waveform_video(
                    self.current_audio_file, output_file)
            elif video_type == "circle":
                output_file = f"video_circle_{timestamp}.mp4"
                self.current_video_file = self.video_generator.create_circle_visualizer(
                    self.current_audio_file, output_file)
            else:  # simple
                output_file = f"video_simple_{timestamp}.mp4"
                self.current_video_file = self.video_generator.create_simple_background(
                    self.current_audio_file, output_file)
            
            if self.current_video_file and os.path.exists(self.current_video_file):
                self.root.after(0, lambda: self.status_label.config(
                    text="✅ Video generated! Ready to upload to YouTube.", fg='#00ff00'))
                self.root.after(0, lambda: self.upload_button.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.generate_button.config(state=tk.NORMAL))
            else:
                self.root.after(0, lambda: self.status_label.config(
                    text="❌ Failed to generate video", fg='#ff4444'))
                self.root.after(0, lambda: self.generate_button.config(state=tk.NORMAL))
                
        except Exception as e:
            print(f"❌ Video generation error: {e}")
            self.root.after(0, lambda: self.status_label.config(
                text=f"❌ Video generation error: {e}", fg='#ff4444'))
            self.root.after(0, lambda: self.generate_button.config(state=tk.NORMAL))
    
    def upload_to_youtube(self):
        """Upload video to YouTube"""
        if not self.current_video_file or not os.path.exists(self.current_video_file):
            messagebox.showerror("Error", "No video file available!")
            return
        
        self.status_label.config(text="📤 Uploading to YouTube...", fg='#ff8800')
        self.upload_button.config(state=tk.DISABLED)
        
        # Upload in separate thread
        upload_thread = threading.Thread(target=self.upload_to_youtube_thread)
        upload_thread.daemon = True
        upload_thread.start()
    
    def upload_to_youtube_thread(self):
        """Upload to YouTube in separate thread"""
        try:
            title = self.title_entry.get()
            description = self.description_text.get("1.0", tk.END).strip()
            privacy = self.privacy_var.get()
            
            video_id = self.youtube_uploader.upload_video(
                self.current_video_file,
                title=title,
                description=description,
                privacy_status=privacy
            )
            
            if video_id:
                self.root.after(0, lambda: self.status_label.config(
                    text=f"✅ Uploaded to YouTube! Video ID: {video_id}", fg='#00ff00'))
                self.root.after(0, lambda: self.upload_button.config(state=tk.NORMAL))
            else:
                self.root.after(0, lambda: self.status_label.config(
                    text="❌ Failed to upload to YouTube", fg='#ff4444'))
                self.root.after(0, lambda: self.upload_button.config(state=tk.NORMAL))
                
        except Exception as e:
            print(f"❌ Upload error: {e}")
            self.root.after(0, lambda: self.status_label.config(
                text=f"❌ Upload error: {e}", fg='#ff4444'))
            self.root.after(0, lambda: self.upload_button.config(state=tk.NORMAL))
    
    def show_youtube_setup(self):
        """Show YouTube setup instructions"""
        setup_window = tk.Toplevel(self.root)
        setup_window.title("YouTube Setup")
        setup_window.geometry("600x400")
        setup_window.configure(bg='#2b2b2b')
        
        # Instructions
        instructions = """
🔐 YouTube API Setup Instructions:

1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
   - Application type: Desktop application
   - Download the JSON file
5. Rename the downloaded file to 'client_secrets.json'
6. Place it in the same directory as this app
7. Click "Create Template" button below to see the expected format

The app will handle the authentication flow automatically.
        """
        
        text_widget = tk.Text(
            setup_window,
            wrap=tk.WORD,
            bg='#2b2b2b',
            fg='#ffffff',
            font=("Arial", 10)
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert("1.0", instructions)
        text_widget.config(state=tk.DISABLED)
        
        # Create template button
        template_button = tk.Button(
            setup_window,
            text="Create Template",
            command=lambda: self.youtube_uploader.create_client_secrets_template(),
            font=("Arial", 12, "bold"),
            bg='#4444ff',
            fg='white'
        )
        template_button.pack(pady=10)
    
    def load_settings(self):
        """Load application settings"""
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_settings(self):
        """Save application settings"""
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def on_closing(self):
        """Handle application closing"""
        self.save_settings()
        self.audio_recorder.cleanup()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = AudioVideoApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()