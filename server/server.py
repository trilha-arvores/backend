from services import FlaskService, DBService
from models import Admin
from controllers.trails import trails_controller

from flask import jsonify, request
import datetime as dt

FlaskService.setup_app()
app = FlaskService.app

app.register_blueprint(trails_controller, url_prefix="/trails")


@app.route('/allAdmin', methods=['GET'])
def all_admin():
    result = Admin.query.all()
    return jsonify(result), 200


@app.route('/newAdmin', methods=['POST'])
def new_admin():
    name = request.json.get('name')
    password = request.json.get('password')

    if name is None or password is None:
        return jsonify({'message': 'Error on body.'}), 401

    new_admin = Admin(
        username=name,
        password=password,
        created_at=dt.datetime.now()
    )

    DBService.session.add(new_admin)
    DBService.session.commit()

    return jsonify({'message': 'Success.'}), 200


@app.route('/admin/<string:name>', methods=['GET'])
def get_admin(name: str):
    admin = Admin.query.filter_by(username=name).first()

    return jsonify(admin), 200


FlaskService.run_app()
