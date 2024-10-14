import os
from flask import Flask
from flask_cors import CORS

from env import getenv

app = None


if app is None:
    server_name = getenv("SERVER_NAME", "Semantic Search Engine")
    print(f"Server Name: {server_name}")
    public_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "public"))
    public_path = getenv("PUBLIC_PATH", public_path)
    app = Flask(
        server_name,
        static_folder=public_path,
        template_folder=public_path,
        static_url_path="/",
    )
    CORS(app)
