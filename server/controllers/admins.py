from flask import Blueprint, jsonify, request
import datetime

from models import Admin, Trail, TreeTrail
from services import AuthenticationService, DBService, ObjectStorageService

admin_controller = Blueprint('admins', __name__)


@admin_controller.route('/trails', methods=['GET'])
def get_all_trails():
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    all_trails = Trail.query.all()
    trails_dict = []
    for trail in all_trails:
        aux_trail = trail.to_dict()
        trees = {}
        trees_in_trail: list[TreeTrail] = TreeTrail.query.filter_by(trail_id=aux_trail["id"]).all()
        for tt in trees_in_trail:
            trees[tt.trail_order] = tt.tree.to_dict()

            trees[tt.trail_order]["distance"] = float(tt.distance) if tt.distance else None
        aux_trail["trees"] = trees
        trails_dict.append(aux_trail)

    return jsonify(trails_dict), 200


@admin_controller.route('/trail/<int:trail_id>', methods=['GET'])
def get_trails(trail_id: int):
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    trail: Trail = Trail.query.filter_by(id=trail_id).one()
    aux_trail = trail.to_dict()
    trees = {}
    trees_in_trail: list[TreeTrail] = TreeTrail.query.filter_by(trail_id=aux_trail["id"]).all()
    for tt in trees_in_trail:
        trees[tt.trail_order] = tt.tree.to_dict()

        trees[tt.trail_order]["distance"] = float(tt.distance) if tt.distance else None
    aux_trail["trees"] = trees

    return jsonify(aux_trail), 200


@admin_controller.route('/create', methods=["POST"])
def create_trail():
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    name = request.json.get("name")
    n_trees = request.json.get("n_trees")
    distance = request.json.get("distance")
    photo = request.json.get("photo")

    trail = Trail(
        name=name,
        n_trees=n_trees,
        distance=distance,
        active=True,
        photo=photo,
        created_at=datetime.datetime.now()
    )
    DBService.session.add(trail)
    DBService.session.commit()

    just_added: Trail = Trail.query.filter_by(name=name).one()
    if just_added is None:
        return "Trail not found", 404

    tree_list = request.json.get("trees")
    if tree_list is None:
        return "Tree list not provided", 400

    for index, value in enumerate(tree_list):
        tree_trail = TreeTrail(
            tree_id=value,
            trail_id=just_added.id,
            trail_order=index,
            active=True,
        )
        DBService.session.add(tree_trail)

    DBService.session.commit()
    return "Created", 201


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


@admin_controller.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    ObjectStorageService.upload_file(file)

    return {}, 200


@admin_controller.route('/url/<file_name>', methods=['GET'])
def get_url(file_name):
    url = ObjectStorageService.get_url(file_name)

    public_url = url.replace('minio:9000', 'localhost:9000')

    return jsonify(public_url), 200
