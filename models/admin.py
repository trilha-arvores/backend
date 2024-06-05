from dataclasses import dataclass
from services import DBService

import datetime as dt


db = DBService.db

@dataclass
class Admin(db.Model):
    __tablename__ = 'admin'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username: str = db.Column(db.Text, nullable=False)
    password: str = db.Column(db.Text, nullable=True)
    created_at: dt.datetime = db.Column(db.DateTime)
