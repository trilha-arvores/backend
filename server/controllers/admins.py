from flask import Blueprint, jsonify, request

from models import Admin, Trail
from services import AuthenticationService, DBService

admin_controller = Blueprint('admins', __name__)


@admin_controller.route('/trails', methods=['GET'])
def get_all_trails():
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    all_trails = Trail.query.all()
    trails_dict = [trail.to_dict() for trail in all_trails]
    return jsonify(trails_dict), 200


@admin_controller.route('/trail/<int:trail_id>', methods=['GET'])
def get_trails(trail_id: int):
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    trail: Trail = Trail.query.filter_by(id=trail_id).one()

    return jsonify(trail.to_dict()), 200


@admin_controller.route('/trail/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id: int):
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    trail: Trail = Trail.query.filter_by(id=trail_id).one()

    DBService.session.delete(trail)
    DBService.session.commit()

    return {}, 200


@admin_controller.route('/login', methods=['POST'])
def login():
    user = request.json.get("username")
    password = request.json.get("password")

    admin: Admin = Admin.query.filter_by(username=user, password=password).first()

    if admin is None:
        return {'message': "No user found"}, 400

    return AuthenticationService.generate_token(admin.id), 200
