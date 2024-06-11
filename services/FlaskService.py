from flask import Flask
from services import DBService
from config import config
from flask_swagger_ui import get_swaggerui_blueprint


class FlaskService:
    app: Flask

    @classmethod
    def setup_app(cls):
        cls.app = Flask(__name__)

        # Swagger setup
        swaggerui_blueprint = get_swaggerui_blueprint(
            '/docs',
            '/static/swagger.json',
            config={
                'app_name': "Trilha das Arvores"
            },
        )

        cls.app.register_blueprint(swaggerui_blueprint)

        db_user = config['db']['user']
        db_password = config['db']['password']
        db_ip = config['db']['ip']
        db_port = config['db']['port']
        db_database = config['db']['database']
        db_uri = f'postgresql://{db_user}:{db_password}@{db_ip}:{db_port}/{db_database}'

        cls.app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        cls.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

        db = DBService.db
        db.init_app(cls.app)

        return cls.app

    @classmethod
    def run_app(cls):
        cls.app.run(host='0.0.0.0', use_reloader=False)
