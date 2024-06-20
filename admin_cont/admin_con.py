import psycopg2 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy import text
from flask import current_app
db=SQLAlchemy()
class con:
    def __init__(self):
        self.connect()

    def con():
        self=db.session()
        self.begin()
        udata=db.session.execute(text("select *from users;"))
        usdata=udata.fetchone()
        self.commit()
        self.close()

