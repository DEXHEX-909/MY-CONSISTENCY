# 🎤 Audio Recorder & YouTube Uploader

A powerful desktop application that records audio, removes silences, creates beautiful video visualizers, and uploads directly to YouTube with just a keyboard shortcut!

## ✨ Features

- **🎤 One-Key Recording**: Press `Ctrl+.` to start/stop recording
- **🔇 Automatic Silence Removal**: Intelligently removes silent parts from your audio
- **🎨 Multiple Video Styles**: Choose from 4 different visualizer types:
  - Audio Visualizer (colorful frequency bars)
  - Waveform (classic audio wave display)
  - Circular Visualizer (expanding circles)
  - Simple Black Background (minimalist)
- **📤 Direct YouTube Upload**: Upload videos directly to YouTube with custom titles, descriptions, and privacy settings
- **🎯 Modern Dark UI**: Beautiful, intuitive interface
- **⚡ Real-time Processing**: All operations run in background threads

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup YouTube API (Optional)

To enable YouTube upload functionality:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
   - Application type: Desktop application
   - Download the JSON file
5. Rename the downloaded file to `client_secrets.json`
6. Place it in the same directory as the app

### 3. Run the Application

```bash
python main_app.py
```

## 🎮 Usage

### Recording Audio
1. **Start Recording**: Press `Ctrl+.` or click the "Start Recording" button
2. **Stop Recording**: Press `Ctrl+.` again or click "Stop Recording"
3. The app automatically processes the audio and removes silences

### Creating Videos
1. **Choose Video Type**: Select your preferred visualizer style
2. **Generate Video**: Click "Generate Video" to create the MP4 file
3. **Preview**: The video will be saved with a timestamp in the filename

### Uploading to YouTube
1. **Enter Details**: Fill in title, description, and privacy settings
2. **Upload**: Click "Upload to YouTube" to publish your video
3. **Monitor**: Watch the progress and get the video URL when complete

## 🎨 Video Styles

### Audio Visualizer
- Colorful frequency bars that respond to audio
- Rainbow gradient colors based on frequency
- Perfect for music and dynamic content

### Waveform
- Classic audio waveform display
- Blue gradient intensity based on amplitude
- Great for podcasts and speech

### Circular Visualizer
- Expanding circles that pulse with audio
- Blue gradient intensity
- Modern, minimalist aesthetic

### Simple Black Background
- Clean black background with audio
- No visual effects, just pure audio
- Perfect for audio-only content

## ⚙️ Configuration

### Audio Settings
- **Sample Rate**: 44.1 kHz
- **Channels**: Mono
- **Format**: 32-bit float
- **Silence Threshold**: -40 dB (adjustable)

### Video Settings
- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30 FPS
- **Codec**: H.264
- **Audio Codec**: AAC

### YouTube Settings
- **Privacy**: Private, Unlisted, or Public
- **Category**: Defaults to "People & Blogs"
- **Made for Kids**: Automatically set to No

## 🔧 Advanced Features

### Keyboard Shortcuts
- `Ctrl+.` - Start/Stop recording
- All other controls available via GUI

### File Management
- Audio files are automatically saved with timestamps
- Video files include visualizer type in filename
- Temporary files are cleaned up automatically

### Error Handling
- Comprehensive error messages
- Graceful failure recovery
- Progress indicators for all operations

## 📁 File Structure

```
audio-recorder-app/
├── main_app.py              # Main application
├── audio_recorder.py        # Audio recording module
├── video_generator.py       # Video generation module
├── youtube_uploader.py      # YouTube upload module
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── client_secrets.json     # YouTube API credentials (user-provided)
├── settings.json           # App settings (auto-generated)
└── token.pickle           # YouTube auth token (auto-generated)
```

## 🛠️ Troubleshooting

### Common Issues

**"No module named 'pyaudio'"**
```bash
# On Ubuntu/Debian:
sudo apt-get install portaudio19-dev python3-pyaudio

# On macOS:
brew install portaudio
pip install pyaudio

# On Windows:
pip install pyaudio
```

**"YouTube API authentication failed"**
- Ensure `client_secrets.json` is in the correct location
- Check that YouTube Data API v3 is enabled in Google Cloud Console
- Delete `token.pickle` and re-authenticate

**"Audio recording not working"**
- Check microphone permissions
- Ensure microphone is not muted
- Try running with sudo (Linux) for audio device access

**"Video generation fails"**
- Ensure sufficient disk space
- Check that all video codecs are installed
- Try a different video type

### Performance Tips

- Close other audio applications while recording
- Use SSD storage for faster video generation
- Ensure stable internet connection for YouTube uploads
- Monitor system resources during video generation

## 🔒 Privacy & Security

- All audio processing is done locally
- YouTube credentials are stored securely
- No data is sent to third parties except YouTube
- Temporary files are automatically cleaned up

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the error messages in the application
3. Ensure all dependencies are properly installed
4. Verify YouTube API setup if using upload feature

---

**Happy Recording! 🎤✨**