from dataclasses import dataclass
from services import DBService

import datetime as dt
from decimal import Decimal


db = DBService.db


@dataclass
class Trail(db.Model):
    __tablename__ = 'trail'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.Text, nullable=False)
    n_trees: int = db.Column(db.Integer, nullable=False)
    distance: float = db.Column(db.Numeric, nullable=False)
    active: bool = db.Column(db.Boolean, nullable=False)
    thumb_img: bytes = db.Column(db.LargeBinary, nullable=True)
    map_img: bytes = db.Column(db.LargeBinary, nullable=True)
    created_at: dt.datetime = db.Column(db.DateTime)

    def to_dict(self):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, Decimal):
                value = float(value)
            result[c.name] = value

        result['thumb_img'] = f"http://localhost:5000/trails/thumb/{result['id']}"
        result['map_img'] = f"http://localhost:5000/trails/map/{result['id']}"

        return result
