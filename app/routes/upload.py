from flask import Blueprint, request, jsonify, Response
from werkzeug.utils import secure_filename
import os
import logging
import mimetypes
import json
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

        # First, validate and save all files
        file_paths = []
        failed_validations = []
        
        for file in files:
            if not file:
                continue

            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            
            # Check file type before saving
            mime_type, _ = mimetypes.guess_type(filename)
            if mime_type not in ["application/pdf", "text/plain"]:
                logger.error(f"Invalid file type for {filename}: {mime_type}")
                failed_validations.append(filename)
                continue

            logger.info(f"Saving file to {file_path}")
            file.save(file_path)
            file_paths.append((file_path, filename))

        # If all files failed validation, return early
        if len(failed_validations) == len(files):
            return jsonify({
                "message": "All files failed validation",
                "successful_uploads": [],
                "failed_uploads": failed_validations
            })

        successful_uploads = []
        failed_uploads = failed_validations.copy()
        total_files = len(file_paths)
        processed_files = 0

        document_processor = ServiceContainer.get_instance().document_processor

        def generate():
            nonlocal processed_files
            
            for file_path, filename in file_paths:
                # Send status update - Starting processing
                yield json.dumps({
                    "status": "processing",
                    "file": filename,
                    "progress": 50 + (processed_files * 50 // total_files)
                }) + "\n"

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

                processed_files += 1

                # Send status update - File complete
                yield json.dumps({
                    "status": "complete",
                    "file": filename,
                    "progress": 50 + (processed_files * 50 // total_files),
                    "successful": filename in successful_uploads
                }) + "\n"

            # Send final status
            yield json.dumps({
                "status": "finished",
                "successful_uploads": successful_uploads,
                "failed_uploads": failed_uploads,
                "progress": 100
            }) + "\n"

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        logger.error(f"Error in upload_file: {str(e)}")
        return jsonify({"error": str(e)}), 500
