from dataclasses import dataclass
from services import DBService


db = DBService.db

@dataclass
class TreeTrail(db.Model):
    __tablename__ = 'tree_trail'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    tree_id: int = db.Column(db.Integer, db.ForeignKey('tree.id'), nullable=False)
    tree = db.relationship("Tree")

    trail_id: int = db.Column(db.Integer, db.ForeignKey('trail.id'), nullable=False)
    trail = db.relationship("Trail")

    trail_order: int = db.Column(db.Integer, nullable=False)
    distance: float = db.Column(db.Numeric, nullable=True)
    active: bool = db.Column(db.Boolean, nullable=False)
