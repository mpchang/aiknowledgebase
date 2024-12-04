import logging
from app import create_app
from app.services.embedding_service import EmbeddingService
from app.services.document_processor import DocumentProcessor
from app.services.container import ServiceContainer
from app.config.config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize services
embedding_service = EmbeddingService()
document_processor = DocumentProcessor(embedding_service)

# Initialize service container
ServiceContainer.initialize(document_processor, embedding_service)

# Create Flask application
app = create_app()

if __name__ == "__main__":
    logger.info(f"Starting server on {Config.HOST}:{Config.PORT}...")
    app.run(host=Config.HOST, port=Config.PORT, debug=True)
