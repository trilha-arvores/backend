from dataclasses import dataclass
from services import DBService

import datetime as dt


db = DBService.db

@dataclass
class Tree(db.Model):
    __tablename__ = 'tree'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    esalq_id: int = db.Column(db.Integer, nullable=False)
    name: str = db.Column(db.Text, nullable=False)
    sci_name: str = db.Column(db.Text, nullable=True)
    loc: str = db.Column(db.Text, nullable=True)
    height: float = db.Column(db.Numeric, nullable=True)
    latitude: float = db.Column(db.Numeric, nullable=True)
    longitude: float = db.Column(db.Numeric, nullable=True)
    active: bool = db.Column(db.Boolean, nullable=False)
    photo: str = db.Column(db.Text, nullable=True)
    created_at: dt.datetime = db.Column(db.DateTime)
    qr_code: str = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
