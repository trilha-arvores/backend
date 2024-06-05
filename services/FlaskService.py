from flask import Flask
from . import DBService


class FlaskService:
    app: Flask

    @classmethod
    def setup_app(cls):
        cls.app = Flask(__name__)

        db_user = 'trilhadasarvores_owner'
        db_password = 'Cu7NfW5acGpi'
        db_ip = 'ep-cool-wave-a4pwyn0v.us-east-1.aws.neon.tech'
        db_port = 5432
        db_database = 'trilhadasarvores'
        db_uri = f'postgresql://{db_user}:{db_password}@{db_ip}:{db_port}/{db_database}'

        cls.app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        cls.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

        db = DBService.db
        db.init_app(cls.app)

        return cls.app

    @classmethod
    def run_app(cls):
        cls.app.run(host='0.0.0.0', use_reloader=False)