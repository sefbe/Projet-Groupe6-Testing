from flask import Blueprint, request, jsonify
from app.models.vehicle import Vehicle
from app import db

vehicle_bp = Blueprint('vehicle', __name__)

# CREATE
@vehicle_bp.route('/vehicle', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    
    new_vehicle = Vehicle(
        registrationNumber=data['registrationNumber'],
        make=data['make'],
        model=data['model'],
        year=data['year'],
        rentalPrice=data['rentalPrice']
    )
    
    db.session.add(new_vehicle)
    db.session.commit()
    
    return jsonify({"message": "Vehicle created", "vehicle": new_vehicle.to_dict()}), 201

# READ ALL
@vehicle_bp.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.to_dict() for vehicle in vehicles]), 200

# READ ONE
@vehicle_bp.route('/vehicle/<int:id>', methods=['GET'])
def get_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    return jsonify(vehicle.to_dict()), 200

# UPDATE
@vehicle_bp.route('/vehicle/<int:id>', methods=['PUT'])
def update_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    data = request.get_json()
    
    if 'registrationNumber' in data:
        vehicle.registrationNumber = data['registrationNumber']
    if 'make' in data:
        vehicle.make = data['make']
    if 'model' in data:
        vehicle.model = data['model']
    if 'year' in data:
        vehicle.year = data['year']
    if 'rentalPrice' in data:
        vehicle.rentalPrice = data['rentalPrice']
    
    db.session.commit()
    return jsonify({"message": "Vehicle updated", "vehicle": vehicle.to_dict()}), 200

# DELETE
@vehicle_bp.route('/vehicle/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted"}), 200

# SEARCH BY REGISTRATION
@vehicle_bp.route('/vehicle/search/<string:registration>', methods=['GET'])
def search_by_registration(registration):
    vehicle = Vehicle.query.filter_by(registrationNumber=registration).first_or_404()
    return jsonify(vehicle.to_dict()), 200

# SEARCH BY PRICE
@vehicle_bp.route('/vehicles/price/<float:max_price>', methods=['GET'])
def search_by_price(max_price):
    vehicles = Vehicle.query.filter(Vehicle.rentalPrice <= max_price).all()
    return jsonify([vehicle.to_dict() for vehicle in vehicles]), 200