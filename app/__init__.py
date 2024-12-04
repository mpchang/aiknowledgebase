from flask import Flask
from flask_cors import CORS
from app.config.config import Config
from app.routes.upload import upload_bp
from app.routes.query import query_bp
from app.routes.files import files_bp
from app.routes.main import main_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(query_bp)
    app.register_blueprint(files_bp)
    
    return app
