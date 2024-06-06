from flask import Blueprint, jsonify, request

from models import Admin, Trail

admin_controller = Blueprint('admins', __name__)

@admin_controller.route('/', methods = ['GET'])
def get_all_trails():
    all_trails = Trail.query.all()
    return jsonify(all_trails), 200

@admin_controller.route('/login', methods = ['POST'])
def if_admin():
    supposed_user = request.json.get("username")
    supposed_ps = request.json.get("password")

    test = Admin.query.filter_by(username=supposed_user, password=supposed_ps).one()
    return jsonify(test), 200

@admin_controller.route('/edit/<int:trail_id>', methods=["POST"])
def get_trail_by_id(trail_id: int):
    trail: Trail = Trail.query.filter_by(trail_id=trail_id).all()
    return jsonify(trail), 200