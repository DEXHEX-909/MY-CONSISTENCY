import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import json

class YouTubeUploader:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        self.API_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.CLIENT_SECRETS_FILE = 'client_secrets.json'
        self.credentials = None
        
    def authenticate(self):
        """Authenticate with YouTube API"""
        print("🔐 Authenticating with YouTube...")
        
        # Check if credentials file exists
        if not os.path.exists(self.CLIENT_SECRETS_FILE):
            print(f"❌ {self.CLIENT_SECRETS_FILE} not found!")
            print("Please download your OAuth 2.0 client credentials from Google Cloud Console")
            print("and save them as 'client_secrets.json' in the same directory")
            return False
        
        # Load existing credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)
        
        # If credentials are invalid or don't exist, get new ones
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRETS_FILE, self.SCOPES)
                self.credentials = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)
        
        print("✅ YouTube authentication successful!")
        return True
    
    def upload_video(self, video_file, title="My Audio Recording", 
                    description="", tags=None, category_id="22", privacy_status="private"):
        """Upload video to YouTube"""
        if not self.authenticate():
            return False
        
        if not os.path.exists(video_file):
            print(f"❌ Video file not found: {video_file}")
            return False
        
        try:
            # Build YouTube service
            youtube = build(self.API_NAME, self.API_VERSION, credentials=self.credentials)
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Create media upload
            media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
            
            print(f"📤 Uploading {video_file} to YouTube...")
            print(f"📝 Title: {title}")
            print(f"🔒 Privacy: {privacy_status}")
            
            # Upload video
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"📊 Upload progress: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"✅ Video uploaded successfully!")
            print(f"🔗 Video URL: {video_url}")
            print(f"🆔 Video ID: {video_id}")
            
            return video_id
            
        except HttpError as e:
            print(f"❌ YouTube API error: {e}")
            return False
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
    
    def create_client_secrets_template(self):
        """Create a template for client_secrets.json"""
        template = {
            "installed": {
                "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
                "project_id": "your-project-id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "YOUR_CLIENT_SECRET",
                "redirect_uris": ["http://localhost"]
            }
        }
        
        with open('client_secrets_template.json', 'w') as f:
            json.dump(template, f, indent=2)
        
        print("📄 Created client_secrets_template.json")
        print("Please replace with your actual OAuth 2.0 credentials from Google Cloud Console")
    
    def get_video_info(self, video_id):
        """Get information about uploaded video"""
        if not self.authenticate():
            return None
        
        try:
            youtube = build(self.API_NAME, self.API_VERSION, credentials=self.credentials)
            
            request = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                snippet = video['snippet']
                statistics = video.get('statistics', {})
                
                print(f"📊 Video Information:")
                print(f"   Title: {snippet['title']}")
                print(f"   Description: {snippet['description'][:100]}...")
                print(f"   Published: {snippet['publishedAt']}")
                print(f"   Views: {statistics.get('viewCount', 'N/A')}")
                print(f"   Likes: {statistics.get('likeCount', 'N/A')}")
                
                return video
            else:
                print("❌ Video not found")
                return None
                
        except HttpError as e:
            print(f"❌ YouTube API error: {e}")
            return None