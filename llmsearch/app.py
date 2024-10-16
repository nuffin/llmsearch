import os
import sys

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from flask import Flask, current_app
from flask.cli import AppGroup
from flask_cors import CORS
import logging
import plotly.express as px

project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)


logging.basicConfig(level=logging.DEBUG)


# Create a custom CLI group
cli = AppGroup("cli")


@cli.command("config")
def dump_config():
    """Show config."""
    print("===================================================================")
    print("Current config:")
    items = current_app.config.items()
    for key, value in items:
        print(f"{key}: {value}")
    print("===================================================================")


def create_app():
    from db import init_db
    from env import getenv
    import web
    import api

    server_name = getenv("SERVER_NAME")
    public_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "public"))
    public_path = getenv("PUBLIC_PATH")
    app = Flask(
        server_name,
        static_folder=public_path,
        template_folder=public_path,
        static_url_path="/",
    )
    app.config.from_object("config.Config")
    CORS(app)

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
                            dbc.Col(
                                html.H1("Simple Dash App", className="text-center")
                            ),
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

    app.register_blueprint(web.bp)
    app.register_blueprint(api.bp)
    app.cli.add_command(cli)

    init_db(app)

    return app


def main():
    ## from filetypes.mimetype import detect

    ## dir = os.path.dirname(__file__)
    ## filepath = os.path.realpath(os.path.join(dir, "..", "requirements.txt"))
    ## print(f"filepath={filepath}")
    ## meme_type = detect(filepath)
    ## print(f"meme_type={meme_type}")

    from env import getenv

    host = getenv("HOST")
    port = getenv("PORT")
    app = create_app()
    app.run(debug=True, host=host, port=port)


if __name__ == "__main__":
    main()
