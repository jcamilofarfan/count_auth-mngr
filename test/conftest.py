import os
os.environ['RUN_ENV'] = 'test'

from src.model import user_model
from src.utils.settings import Settings

from src.utils.db import db

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

settings = Settings()


def postgresql_connection():
    con = psycopg2.connect(f"user='{settings.db_user}' password='{settings.db_pass}'")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return con

def delete_tables():
    with db:
        result = db.table_exists(user_model.User)
        if result:
            db.drop_tables([user_model.User])

def pytest_sessionstart(session):
    delete_tables()
    with db:
        db.create_tables([user_model.User])


def pytest_sessionfinish(session, exitstatus):
    delete_tables()

