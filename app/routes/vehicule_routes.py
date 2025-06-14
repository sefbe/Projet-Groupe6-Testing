from flask import Blueprint, request, jsonify
from app.models.vehicule import db, Vehicle
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

vehicule_bp = Blueprint('vehicule_bp', __name__, url_prefix='/vehicles')

"""
# Décorateur pour vérifier le rôle admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user and user.role == "admin":
            return fn(*args, **kwargs)
        return jsonify({"error": "Accès réservé aux administrateurs"}), 403
    return wrapper

"""
# Create a vehicle (admin only)
@vehicule_bp.route('', methods=['POST'])
@jwt_required()
def create_vehicle():
    data = request.get_json()

    required_fields = ['registrationNumber', 'make', 'model', 'year', 'rentalPrice']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        vehicle = Vehicle(
            registrationNumber=data['registrationNumber'],
            make=data['make'],
            model=data['model'],
            year=data['year'],
            rentalPrice=data['rentalPrice']
        )
        db.session.add(vehicle)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({'message': 'Vehicle created successfully'}), 201


# Get all vehicles (auth required)
@vehicule_bp.route('', methods=['GET'])
@jwt_required()
def get_vehicles():
    vehicles = Vehicle.query.all()
    vehicles_list = [{
        'id': v.id,
        'registrationNumber': v.registrationNumber,
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'rentalPrice': v.rentalPrice
    } for v in vehicles]
    return jsonify({'vehicles': vehicles_list}), 200
    
@vehicule_bp.route('/<int:vehicle_id>', methods=['GET'])
@jwt_required()
def get_vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"message": "Vehicle not found"}), 404

    vehicle_data = {
        "id": vehicle.id,
        "registrationNumber": vehicle.registrationNumber,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "rentalPrice": vehicle.rentalPrice
    }
    return jsonify({"vehicle": vehicle_data}), 200




# Update a vehicle by ID (admin only)
@vehicule_bp.route('/<int:vehicle_id>', methods=['PUT'])
@jwt_required()
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"message": "Vehicle not found"}), 404

    data = request.get_json()
    vehicle.registrationNumber = data.get('registrationNumber', vehicle.registrationNumber)
    vehicle.make = data.get('make', vehicle.make)
    vehicle.model = data.get('model', vehicle.model)
    vehicle.year = data.get('year', vehicle.year)
    vehicle.rentalPrice = data.get('rentalPrice', vehicle.rentalPrice)
    db.session.commit()

    vehicle_data = {
        "id": vehicle.id,
        "registrationNumber": vehicle.registrationNumber,
        "make": vehicle.make,
        "model": vehicle.model,
        "year": vehicle.year,
        "rentalPrice": vehicle.rentalPrice
    }

    return jsonify({'message': 'Vehicle updated successfully', 'vehicle': vehicle_data})


# Delete a vehicle by ID (admin only)
@vehicule_bp.route('/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"message": "Vehicle not found"}), 404
    
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle deleted successfully'})


# Search by registration number (auth required)
@vehicule_bp.route('/search/registration/<string:registration_number>', methods=['GET'])
@jwt_required()
def search_by_registration(registration_number):
    vehicle = Vehicle.query.filter_by(registrationNumber=registration_number).first()
    if not vehicle:
        return jsonify({'message': 'Vehicle not found'}), 404
    return jsonify({
        'id': vehicle.id,
        'registrationNumber': vehicle.registrationNumber,
        'make': vehicle.make,
        'model': vehicle.model,
        'year': vehicle.year,
        'rentalPrice': vehicle.rentalPrice
    })

# Search by rental price (auth required)
@vehicule_bp.route('/search/price/<float:price>', methods=['GET'])
@jwt_required()
def search_by_price(price):
    vehicles = Vehicle.query.filter(Vehicle.rentalPrice <= price).all()
    return jsonify([{
        'id': v.id,
        'registrationNumber': v.registrationNumber,
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'rentalPrice': v.rentalPrice
    } for v in vehicles])

