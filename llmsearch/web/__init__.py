from flask import (
    Blueprint,
    redirect,
    render_template_string,
    request,
    send_from_directory,
    session,
    url_for,
)

bp = Blueprint("web", __name__, url_prefix="")


# @web_blueprint.route("/")
# def home():
#     return render_template_string(
#         """
#     <h1>Welcome to the Flask + Dash Web App</h1>
#     <p>This page is served by Flask.</p>
#     <p>Click here to go to <a href="/dash/">the Dash app</a>.</p>
#     """
#     )
@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def serve_react_app(path):
    return send_from_directory(bp.static_folder, "index.html")


@bp.route("/login", methods=["GET", "POST"])
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


@bp.route("/logout")
def logout():
    session.pop("username", None)  # Remove username from session
    return redirect(url_for("home"))


@bp.route("/session-data", methods=["GET"])
def get_session_data():
    # Get session data
    return jsonify({"session": dict(session)})


# Flask route for other Flask-only page
@bp.route("/about")
def about():
    return render_template_string(
        """
    <h1>About Page</h1>
    <p>This page is just Flask without Dash content.</p>
    <p><a href="/">Back to home</a></p>
    """
    )
