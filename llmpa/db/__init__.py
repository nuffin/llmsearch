def insert_path():
    import os
    import sys

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


insert_path()
del insert_path

from .postgres import db, async_engine, async_session, init_db
from . import schemas
