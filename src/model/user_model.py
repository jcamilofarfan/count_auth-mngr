from operator import index
import peewee

from src.utils.db import db

class User(peewee.Model):
    email = peewee.CharField(unique=True, index=True)
    username = peewee.CharField(unique=True, index=True)
    password = peewee.CharField()
    status = peewee.BooleanField(default=True)
    created_at = peewee.DateTimeField(default=peewee.datetime.datetime.now)
    updated_at = peewee.DateTimeField(default=peewee.datetime.datetime.now)

    class Meta:
        database = db