#!/usr/bin/env python3
"""
Audio Recorder & YouTube Uploader Launcher
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'pyaudio', 'numpy', 'scipy', 'librosa', 'moviepy', 
        'opencv-python', 'matplotlib', 'keyboard', 'pillow',
        'google-api-python-client', 'google-auth-oauthlib', 
        'google-auth-httplib2', 'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing missing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main launcher function"""
    print("🎤 Audio Recorder & YouTube Uploader")
    print("=" * 50)
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"⚠️ Missing dependencies: {', '.join(missing)}")
        response = input("Would you like to install them now? (y/n): ")
        
        if response.lower() in ['y', 'yes']:
            if not install_dependencies():
                print("❌ Failed to install dependencies. Please install them manually:")
                print("pip install -r requirements.txt")
                return
        else:
            print("❌ Cannot run without required dependencies.")
            return
    
    # Check for audio device
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        
        if device_count == 0:
            print("⚠️ No audio devices found!")
            print("Please ensure your microphone is connected and working.")
            return
    except Exception as e:
        print(f"⚠️ Could not check audio devices: {e}")
    
    # Start the application
    print("🚀 Starting application...")
    print("💡 Press Ctrl+. to start/stop recording")
    print("💡 Use the GUI for video generation and YouTube upload")
    print("-" * 50)
    
    try:
        from main_app import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        print("Please check the error message above and try again.")

if __name__ == "__main__":
    main()