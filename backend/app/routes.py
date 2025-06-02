from flask import Blueprint, request, jsonify
from .crud import get_vehicle_by_id, create_vehicle, update_vehicle, delete_vehicle, get_all_vehicles, find_by_registration_number, find_by_price

routes = Blueprint('routes', __name__)

@routes.route('/vehicles', methods=['GET'])
def list_vehicles():
    return jsonify([v.__dict__ for v in get_all_vehicles()])

@routes.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    return jsonify(vehicle.__dict__) if vehicle else ("Not Found", 404)

@routes.route('/vehicles', methods=['POST'])
def add_vehicle():
    vehicle = create_vehicle(request.json)
    return jsonify(vehicle.__dict__), 201

@routes.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update(vehicle_id):
    return jsonify(update_vehicle(vehicle_id, request.json).__dict__)

@routes.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete(vehicle_id):
    delete_vehicle(vehicle_id)
    return '', 204

@routes.route('/vehicles/search/registration', methods=['GET'])
def search_by_registration():
    reg = request.args.get('reg')
    vehicle = find_by_registration_number(reg)
    return jsonify(vehicle.__dict__) if vehicle else ("Not Found", 404)

@routes.route('/vehicles/search/price', methods=['GET'])
def search_by_price():
    price = float(request.args.get('price'))
    vehicles = find_by_price(price)
    return jsonify([v.__dict__ for v in vehicles])
