from flask import Blueprint, jsonify, request

from models import Trail, TreeTrail

trails_controller = Blueprint('trails', __name__)


@trails_controller.route('/', methods=['GET'])
def get_all_trails():
    trails = Trail.query.all()
    return jsonify(trails), 200


@trails_controller.route('/<int:trail_id>', methods=['GET'])
def get_trail_by_id(trail_id: int):
    trail: Trail = Trail.query.filter_by(id=trail_id).one()

    return jsonify(trail), 200


@trails_controller.route('/<int:trail_id>/trees', methods=['GET'])
def get_trail_trees_by_id(trail_id: int):
    trees = []

    trees_in_trail: list[TreeTrail] = TreeTrail.query.filter_by(trail_id=trail_id).all()
    for tt in trees_in_trail:
        trees.append(tt.tree)

    return jsonify(trees), 200


@trails_controller.route('/<int:trail_id>/validate-qr', methods=['POST'])
def validate_qr_and_position(trail_id: int):
    qr_data = request.json.get('qr_data')
    player_pos = int(request.json.get('player_pos'))

    # TODO Validate

    tree_esalq_id = int(qr_data.split('=')[1])

    tt: TreeTrail = TreeTrail.query.filter_by(trail_id=trail_id, trail_order=player_pos).one()

    if tt.tree.esalq_id == tree_esalq_id:
        return jsonify(tt.tree), 200

    else:
        return {}, 400

