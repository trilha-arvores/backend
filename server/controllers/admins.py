import json

from flask import Blueprint, jsonify, request, Response
import datetime
import math

from models import Admin, Trail, TreeTrail
from services import AuthenticationService, DBService

admin_controller = Blueprint('admins', __name__)


def get_haversine_distance(lat1, lon1, lat2, lon2):
    # Converte de graus para radianos
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Diferenças das coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula do haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Raio da Terra em km
    R = 6371.0

    # Distância em km
    distance = R * c

    return distance


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

    name = request.form.get("name")
    tree_list = json.loads(request.form.get("trees"))

    thumb_img = request.files['thumb_img']
    thumb_img_data = thumb_img.read()

    map_img = request.files['map_img']
    map_img_data = map_img.read()

    if tree_list is None:
        return "Tree list not provided", 400

    trail = Trail(
        name=name,
        n_trees=len(tree_list),
        active=True,
        distance=10,
        thumb_img=thumb_img_data,
        map_img=map_img_data,
        created_at=datetime.datetime.now()
    )
    DBService.session.add(trail)

    for index, tree in enumerate(tree_list):
        tree_trail = TreeTrail(
            tree_id=tree,
            trail=trail,
            trail_order=index,
            active=True,
        )
        DBService.session.add(tree_trail)

    DBService.session.commit()
    return "Created", 201


@admin_controller.route('/trail/<int:trail_id>', methods=['PATCH'])
def update_trail(trail_id: int):

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

        trail.n_trees = len(trees)
        TreeTrail.query.filter_by(trail_id=trail_id).delete()
        for index, tree in enumerate(trees):
            tree_trail = TreeTrail(
                tree_id=tree,
                trail=trail,
                trail_order=index,
                active=True,
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
