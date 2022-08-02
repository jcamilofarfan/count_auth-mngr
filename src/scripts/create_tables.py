from src.model.user_model import User

from src.utils.db import db

def create_tables():
    with db:
        db.create_tables([User])