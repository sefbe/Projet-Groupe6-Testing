from flask import Blueprint, request, jsonify
from .models import Vehicle
from .Tested_Crud import get_vehicle_by_id, create_vehicle, update_vehicle, delete_vehicle, get_all_vehicles, find_by_registration_number, find_by_price

routes = Blueprint('routes', __name__)

@routes.route('/vehicles', methods=['GET'])
def list_vehicles():
    vehicles = get_all_vehicles()
    return jsonify([v.to_dict() for v in vehicles])

@routes.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    v = get_vehicle_by_id(vehicle_id)
    return (jsonify(v.to_dict()), 200) if v else ("Not found", 404)

@routes.route('/vehicles', methods=['POST'])
def add_vehicle():
    try:
        data = request.get_json()

        existing = Vehicle.query.filter_by(registration_number=data.get("registration_number")).first()
        if existing:
            return jsonify({"error": "Un vehicule avec ce numero d'immatriculation existe deja."}), 409

        vehicle = create_vehicle(data)
        return jsonify(vehicle.to_dict()), 201

    except KeyError as e:
        return jsonify({"error": f"Champ manquant : {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

@routes.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update(vehicle_id):
    try:
        data = request.get_json()
        v = update_vehicle(vehicle_id, data)
        if not v:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify(v.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@routes.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete(vehicle_id):
    if delete_vehicle(vehicle_id):
        return '', 204
    return jsonify({"error": "Vehicle not found"}), 404

@routes.route('/vehicles/search/registration', methods=['GET'])
def search_by_registration():
    reg = request.args.get('reg')
    if not reg:
        return jsonify({"error": "Missing query param 'reg'"}), 400
    v = find_by_registration_number(reg)
    return (jsonify(v.to_dict()), 200) if v else ("Not found", 404)

@routes.route('/vehicles/search/price', methods=['GET'])
def search_by_price():
    try:
        price = float(request.args.get("price"))
        vehicles = find_by_price(price)
        return jsonify([v.to_dict() for v in vehicles]), 200
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid price value"}), 400
