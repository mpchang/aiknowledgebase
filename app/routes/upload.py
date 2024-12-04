from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
import mimetypes
from app.config.config import Config
from app.services.container import ServiceContainer

logger = logging.getLogger(__name__)

upload_bp = Blueprint('upload', __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    try:
        logger.info("Received file upload request")
        if "files[]" not in request.files:
            logger.error("No files part in request")
            return jsonify({"error": "No files part"}), 400

        files = request.files.getlist("files[]")
        if not files or files[0].filename == "":
            logger.error("No selected files")
            return jsonify({"error": "No selected files"}), 400

        successful_uploads = []
        failed_uploads = []

        document_processor = ServiceContainer.get_instance().document_processor

        for file in files:
            if not file:
                continue

            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            
            # Check file type before saving
            mime_type, _ = mimetypes.guess_type(filename)
            if mime_type not in ["application/pdf", "text/plain"]:
                logger.error(f"Invalid file type for {filename}: {mime_type}")
                failed_uploads.append(filename)
                continue

            logger.info(f"Saving file to {file_path}")
            file.save(file_path)

            metadata = document_processor.process_file(file_path)
            if metadata:
                logger.info(f"File {filename} processed successfully")
                successful_uploads.append(filename)
            else:
                logger.error(f"Error processing file {filename}")
                failed_uploads.append(filename)
                # Clean up failed file
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.error(f"Error removing failed file {file_path}: {str(e)}")

        return jsonify({
            "message": f"Processed {len(successful_uploads)} files successfully",
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads
        })

    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}")
        return jsonify({"error": str(e)}), 500
