from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from env import getenv


db = SQLAlchemy(session_options={"class_": AsyncSession})

DATABASE_URI = getenv("DATABASE_URI")
async_engine = create_async_engine(DATABASE_URI, future=True, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


def init_models():
    from models import File, User

    __models = [File, User]


def init_db(app: Flask):
    global async_engine, async_session

    init_models()

    db.init_app(app)

    # Optionally: attach the async session to the app if needed for use in other parts of the app
    app.async_session = async_session

    ## Create table or migrate with alembic
    # with app.app_context():
    #     db.create_all()
