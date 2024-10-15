import os

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from flask import (
    jsonify,
    redirect,
    render_template_string,
    request,
    send_from_directory,
    session,
    url_for,
)
import hashlib
import logging
import plotly.express as px
from werkzeug.utils import secure_filename

from common import app
from env import getenv
from db import init_db


logging.basicConfig(level=logging.DEBUG)


dash_app = Dash(
    __name__,
    server=app,
    routes_pathname_prefix="/dash/",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

df = px.data.iris()  # Iris dataset (preloaded in Plotly)
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

dash_app.layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(html.H1("Simple Dash App", className="text-center")),
                        dbc.Col(
                            html.P(
                                "This is a simple web app using Flask and Dash.",
                                className="text-center",
                            )
                        ),
                    ]
                ),
                dbc.Row([dbc.Col(dcc.Graph(figure=fig))]),
            ]
        )
    ]
)


# @app.route("/")
# def home():
#     return render_template_string(
#         """
#     <h1>Welcome to the Flask + Dash Web App</h1>
#     <p>This page is served by Flask.</p>
#     <p>Click here to go to <a href="/dash/">the Dash app</a>.</p>
#     """
#     )
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react_app(path):
    return send_from_directory(app.static_folder, "index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if the user exists and the password is correct
        if username in users and users[username] == password:
            session["username"] = username  # Store username in session
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password."

    return """
        <form method="POST">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Log In">
        </form>
    """


@app.route("/logout")
def logout():
    session.pop("username", None)  # Remove username from session
    return redirect(url_for("home"))


@app.route("/session-data", methods=["GET"])
def get_session_data():
    # Get session data
    return jsonify({"session": dict(session)})


# Flask route for other Flask-only page
@app.route("/about")
def about():
    return render_template_string(
        """
    <h1>About Page</h1>
    <p>This page is just Flask without Dash content.</p>
    <p><a href="/">Back to home</a></p>
    """
    )


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

UPLOAD_FOLDER = getenv("UPLOADS_PATH", "data/uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to check allowed file extensions
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])

        temp_path = os.path.join(
            app.config["UPLOAD_FOLDER"], secure_filename(file.filename)
        )
        file.save(temp_path)

        hash_object = hashlib.sha256()
        with open(temp_path, "rb") as f:
            hash_object.update(f.read())

        hashed_filename = hash_object.hexdigest() + os.path.splitext(file.filename)[1]
        hashed_path = os.path.join(app.config["UPLOAD_FOLDER"], hashed_filename)

        os.rename(temp_path, hashed_path)

        return (
            jsonify(
                {"message": "File uploaded successfully", "filename": hashed_filename}
            ),
            201,
        )
    else:
        return jsonify({"error": "File type not allowed"}), 400


init_db()


def main():
    from filetypes.mimetype import detect

    dir = os.path.dirname(__file__)
    filepath = os.path.realpath(os.path.join(dir, "..", "requirements.txt"))
    print(f"filepath={filepath}")
    meme_type = detect(filepath)
    print(f"meme_type={meme_type}")

    app.run(debug=True)


if __name__ == "__main__":
    main()
