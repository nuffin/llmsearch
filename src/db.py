from env import getenv

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db():
    from app import app

    DATABASE_URL = getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": getenv(
            "SQLALCHEMY_ENGINE_POOL_SIZE", 10
        ),  # Pool size (number of connections to keep in the pool)
        "max_overflow": getenv(
            "SQLALCHEMY_ENGINE_MAX_OVERFLOW", 5
        ),  # Allow up to 5 additional connections beyond pool_size
        "pool_timeout": getenv(
            "SQLALCHEMY_ENGINE_POOL_TIMEOUT", 30
        ),  # Wait 30 seconds for a connection before giving up
        "pool_recycle": getenv(
            "SQLALCHEMY_ENGINE_POOL_RECYCLE", 1800
        ),  # Recycle connections after 30 minutes (1800 seconds)
        "pool_pre_ping": getenv(
            "SQLALCHEMY_ENGINE_POOL_PRE_PING", True
        ),  # Enable pre-ping to ensure connections are valid
    }

    from models import File, User

    __models = [File, User]

    db.init_app(app)

    # with app.app_context():
    #     db.create_all()
