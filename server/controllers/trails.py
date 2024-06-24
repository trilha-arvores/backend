from flask import Blueprint, jsonify, request, Response

from models import Trail, TreeTrail
from services import DBService

trails_controller = Blueprint('trails', __name__)


@trails_controller.route('/', methods=['GET'])
def get_all_trails():
    all_trails = Trail.query.all()
    trails_dict = [trail.to_dict() for trail in all_trails]
    return jsonify(trails_dict), 200


@trails_controller.route('/<int:trail_id>', methods=['GET'])
def get_trail_by_id(trail_id: int):
    trail: Trail = Trail.query.filter_by(id=trail_id).one()

    return jsonify(trail.to_dict()), 200


@trails_controller.route('/<int:trail_id>/trees', methods=['GET'])
def get_trail_trees_by_id(trail_id: int):
    trees = {}

    trees_in_trail: list[TreeTrail] = TreeTrail.query.filter_by(trail_id=trail_id).all()
    for tt in trees_in_trail:
        trees[tt.trail_order] = tt.tree.to_dict()

        trees[tt.trail_order]["distance"] = float(tt.distance) if tt.distance else None

    return jsonify(trees), 200


@trails_controller.route('/<int:trail_id>/validate-qr', methods=['POST'])
def validate_qr_and_position(trail_id: int):
    qr_data = request.json.get('qr_data')
    player_pos = int(request.json.get('player_pos'))

    tree_esalq_id = int(qr_data.split('=')[1])
    # TODO Validate

    tt: TreeTrail = TreeTrail.query.filter_by(trail_id=trail_id, trail_order=player_pos).one()

    if tt.tree.esalq_id == tree_esalq_id:
        return jsonify(tt.tree), 200

    else:
        return {'message': f'Expected esald_id {tt.tree.esalq_id} for {player_pos}-th tree. '
                           f'Got {tree_esalq_id} instead.'}, 400


@trails_controller.route('/thumb/<int:trail_id>', methods=['GET'])
def get_thumb_image(trail_id):
    trail = DBService.session.query(Trail).filter_by(id=trail_id).first()
    if not trail or not trail.thumb_img:
        return "Image not found", 404

    return Response(trail.thumb_img, mimetype='image/jpeg')


@trails_controller.route('/map/<int:trail_id>', methods=['GET'])
def get_map_image(trail_id):
    trail = DBService.session.query(Trail).filter_by(id=trail_id).first()
    if not trail or not trail.map_img:
        return "Image not found", 404

    return Response(trail.map_img, mimetype='image/jpeg')
