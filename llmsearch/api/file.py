import os

from flask import (current_app, jsonify, request)
import hashlib
from werkzeug.utils import secure_filename

from env import getenv
from .blueprint import bp

@bp.route('/upload', methods=['POST'])
def upload():
    return jsonify(message='Search'), 200

ALLOWED_EXTENSIONS = {
    "txt",
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "mp4",
    "mp3",
    "mkv",
    "avi",
    "mov",
}  # Allowed file types

# UPLOAD_FOLDER = getenv("UPLOADS_PATH", "data/uploads")
# current_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to check allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        if not os.path.exists(current_app.config["UPLOAD_FOLDER"]):
            os.makedirs(current_app.config["UPLOAD_FOLDER"])

        temp_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], secure_filename(file.filename)
        )
        file.save(temp_path)

        hash_object = hashlib.sha256()
        with open(temp_path, "rb") as f:
            hash_object.update(f.read())

        hashed_filename = hash_object.hexdigest() + os.path.splitext(file.filename)[1]
        hashed_path = os.path.join(current_app.config["UPLOAD_FOLDER"], hashed_filename)

        os.rename(temp_path, hashed_path)

        return (
            jsonify(
                {"message": "File uploaded successfully", "filename": hashed_filename}
            ),
            201,
        )
    else:
        return jsonify({"error": "File type not allowed"}), 400


