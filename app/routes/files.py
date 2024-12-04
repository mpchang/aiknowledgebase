from flask import Blueprint, jsonify
import os
from app.config.config import Config

files_bp = Blueprint('files', __name__)

@files_bp.route("/files", methods=["GET"])
def list_files():
    try:
        files = []
        for filename in os.listdir(Config.UPLOAD_FOLDER):
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                files.append(filename)
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
