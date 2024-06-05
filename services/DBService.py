from flask_sqlalchemy import SQLAlchemy


class DBService:
    db = SQLAlchemy()
    session = db.session
