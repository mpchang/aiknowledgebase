import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    PORT = int(os.getenv('PORT', '5001'))  # Default to port 5001 instead of 5000
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # OpenAI configuration
    API_KEY = os.getenv("API_KEY")
    
    # Embedding configuration
    SIMILARITY_THRESHOLD = 0.3
    MAX_CONTEXT_LENGTH = 4000
    
    # Ensure upload directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
