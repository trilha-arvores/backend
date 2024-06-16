from flask import Blueprint, jsonify, request

from models import Admin, Trail

admin_controller = Blueprint('admins', __name__)

@admin_controller.route('/trails', methods = ['GET'])
def get_all_trails():
    all_trails = Trail.query.all()
    trails_dict = [trail.to_dict() for trail in all_trails]
    return jsonify(trails_dict), 200


@admin_controller.route('/trail/<int:trail_id>', methods = ['GET'])
def get_trails(trail_id: int):
    trail: Trail = Trail.query.filter_by(id=trail_id).one()

    return jsonify(trail), 200

@admin_controller.route('/login', methods = ['POST'])
def if_admin():
    supposed_user = request.json.get("username")
    supposed_ps = request.json.get("password")

    test = Admin.query.filter_by(username=supposed_user, password=supposed_ps).one()
    return jsonify(test), 200
