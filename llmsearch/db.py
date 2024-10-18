from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


db = SQLAlchemy(session_options={"class_": AsyncSession})

async_engine = None
async_session = None

def init_models():
    from models import File, User
    __models = [File, User]


def init_db(app):
    global async_engine, async_session

    async_engine = create_async_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    db.init_app(app)

    # Optionally: attach the async session to the app if needed for use in other parts of the app
    # app.async_session = async_session

    ## Create table or migrate with alembic
    # with app.app_context():
    #     db.create_all()
