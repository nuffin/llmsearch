from flask import Flask
from flask_cors import CORS

from env import getenv

app = None


if app is None:
    server_name = getenv("SERVER_NAME", "Semantic Search Engine")
    print(f"Server Name: {server_name}")
    app = Flask(server_name)
    CORS(app)
