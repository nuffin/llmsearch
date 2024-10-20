import os
import sys

from asgiref.wsgi import WsgiToAsgi
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from flask import Flask, current_app, request
from flask.cli import AppGroup
from flask_cors import CORS
import logging
import plotly.express as px

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
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

    app.config["DEBUG"] = eval(getenv("DEBUG"))

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
    app.register_blueprint(api.bp, url_prefix="/api")
    app.cli.add_command(cli)

    init_db(app)

    # Add a route to print the routing table
    @app.route("/routes")
    def list_routes():
        output = []
        for rule in app.url_map.iter_rules():
            methods = ",".join(rule.methods)
            output.append(f"{rule.endpoint}: {rule} [{methods}]")

        return "<br>".join(output)

    ## @app.before_request
    ## def log_request_info():
    ##     app.logger.debug('Headers: %s', request.headers)
    ##     app.logger.debug('Body: %s', request.get_data())

    for rule in app.url_map.iter_rules():
        methods = ",".join(rule.methods)
        print(f"{rule.endpoint}: {rule} [{methods}]")

    app.config["SERVER_NAME"] = None

    return app


app = create_app()
asgiapp = WsgiToAsgi(app)


def main():
    from env import getenv

    host = getenv("HOST")
    port = getenv("PORT")
    app.run(debug=True, host=host, port=port)


if __name__ == "__main__":
    main()
