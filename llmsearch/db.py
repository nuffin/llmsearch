from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_db(app):
    from models import File, Task, User

    __models = [File, Task, User]

    db.init_app(app)

    ## Create table or migrate with alembic
    # with app.app_context():
    #     db.create_all()
