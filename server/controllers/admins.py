import json

from flask import Blueprint, jsonify, request, Response
import datetime

from models import Admin, Trail, TreeTrail, Tree
from services import AuthenticationService, DBService, MapService

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


@admin_controller.route('/esalqid/<int:esalq_id>', methods=['GET'])
def get_tree_by_esalq_id(esalq_id: int):
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    tree: Tree = Tree.query.filter_by(esalq_id=esalq_id).first()

    if tree is None:
        return "Not found", 404

    return jsonify(tree.to_dict()), 200

@admin_controller.route('/create', methods=["POST"])
def create_trail():
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    name = request.form.get("name")
    tree_list = json.loads(request.form.get("trees"))

    thumb_img = request.files['thumb_img']
    thumb_img_data = thumb_img.read()

    map_img = request.files['map_img']
    map_img_data = map_img.read()

    if tree_list is None:
        return "Tree list not provided", 400

    trees = []
    for tree_id in tree_list:
        tree: Tree = Tree.query.filter_by(id=tree_id).one()
        trees.append(tree)

    distance = 0.0
    for i in range(1, len(tree_list)):
        distance += MapService.get_haversine_distance(
            trees[i - 1].latitude, trees[i - 1].longitude, trees[i].latitude, trees[i].longitude)

    trail = Trail(
        name=name,
        n_trees=len(tree_list),
        active=True,
        distance=distance,
        thumb_img=thumb_img_data,
        map_img=map_img_data,
        created_at=datetime.datetime.now()
    )
    DBService.session.add(trail)

    for index, tree in enumerate(tree_list):
        distance = MapService.get_haversine_distance(
            trees[index - 1].latitude, trees[index - 1].longitude,
            trees[index].latitude, trees[index].longitude) if index != 0 else None

        tree_trail = TreeTrail(
            tree_id=tree,
            trail=trail,
            trail_order=index,
            active=True,
            distance=distance
        )
        DBService.session.add(tree_trail)

    DBService.session.commit()
    return "Created", 201


@admin_controller.route('/trail/<int:trail_id>', methods=['PATCH'])
def update_trail(trail_id: int):
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    trail: Trail = Trail.query.filter_by(id=trail_id).one()

    if name := request.form.get('name'):
        trail.name = name
    if active := request.form.get('active'):
        trail.active = active
    if thumb_img := request.files.get('thumb_img'):
        thumb_img_data = thumb_img.read()
        trail.thumb_img = thumb_img_data
    if map_img := request.files.get('map_img'):
        map_img_data = map_img.read()
        trail.map_img = map_img_data
    if trees := request.form.get("trees"):
        trees = json.loads(trees)

        tree_list = []
        for tree_id in trees:
            tree: Tree = Tree.query.filter_by(id=tree_id).one()
            tree_list.append(tree)

        distance = 0.0
        for i in range(1, len(trees)):
            distance += MapService.get_haversine_distance(
                tree_list[i - 1].latitude, tree_list[i - 1].longitude, tree_list[i].latitude, tree_list[i].longitude)

        trail.n_trees = len(trees)
        trail.distance = distance

        TreeTrail.query.filter_by(trail_id=trail_id).delete()
        for index, tree in enumerate(trees):
            distance = MapService.get_haversine_distance(
                tree_list[index - 1].latitude, tree_list[index - 1].longitude,
                tree_list[index].latitude, tree_list[index].longitude) if index != 0 else None

            tree_trail = TreeTrail(
                tree_id=tree,
                trail=trail,
                trail_order=index,
                active=True,
                distance=distance
            )
            DBService.session.add(tree_trail)

    DBService.session.commit()
    return "Updated", 201


@admin_controller.route('/trail/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id: int):
    try:
        AuthenticationService.authenticate(request)
    except Exception as e:
        return {'message': repr(e)}, 401

    trail: Trail = Trail.query.filter_by(id=trail_id).one()

    TreeTrail.query.filter_by(trail_id=trail_id).delete()

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
