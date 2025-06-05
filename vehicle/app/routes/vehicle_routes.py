# vehicle_routes.py

from flask import Blueprint, request, jsonify
from app.models.vehicle import Vehicle  # Assure-toi que ce modèle existe avec les bons champs
from app import db  # SQLAlchemy

vehicle_bp = Blueprint('vehicle', __name__)

# Healthcheck
@vehicle_bp.route('/', methods=['GET'])
def healthcheck():
    return jsonify({"status": "OK"}), 200

# Get all vehicles
@vehicle_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([v.to_dict() for v in vehicles]), 200

# Get vehicle by ID
@vehicle_bp.route('/vehicle/<int:id>', methods=['GET'])
def get_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    return jsonify(vehicle.to_dict()), 200

# Create new vehicle
@vehicle_bp.route('/vehicle/create', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    vehicle = Vehicle(**data)
    db.session.add(vehicle)
    db.session.commit()
    return jsonify(vehicle.to_dict()), 201

# Update vehicle by ID
@vehicle_bp.route('/vehicle/update/<int:id>', methods=['PUT'])
def update_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(vehicle, key, value)
    db.session.commit()
    return jsonify(vehicle.to_dict()), 200

# Delete vehicle by ID
@vehicle_bp.route('/vehicle/delete/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted"}), 200

# Search by registration number
@vehicle_bp.route('/vehicle/search/<string:registrationNumber>', methods=['GET'])
def search_vehicle_by_registration(registrationNumber):
    vehicle = Vehicle.query.filter_by(registration_number=registrationNumber).first()
    print(f"Vehicle found: {vehicle}")  # Log pour vérifier si le véhicule est trouvé

    if not vehicle:
        return jsonify({"message": "Vehicle not found"}), 404
    return jsonify(vehicle.to_dict()), 200

# Get all vehicles with price <= maxPrice
@vehicle_bp.route('/vehicles/price/<int:maxPrice>', methods=['GET'])
def get_vehicles_by_max_price(maxPrice):
    vehicles = Vehicle.query.filter(Vehicle.rental_price <= maxPrice).all()
    return jsonify([v.to_dict() for v in vehicles]), 200

