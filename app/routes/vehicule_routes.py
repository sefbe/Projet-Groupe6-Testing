from flask import Blueprint, request, jsonify
from app.models.vehicule import db, Vehicle
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

vehicule_bp = Blueprint('vehicule_bp', __name__, url_prefix='/vehicles')

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

# Create a vehicle (admin only)
@vehicule_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
def create_vehicle():
    data = request.get_json()
    vehicle = Vehicle(
        registrationNumber=data['registrationNumber'],
        make=data['make'],
        model=data['model'],
        year=data['year'],
        rentalPrice=data['rentalPrice']
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle created successfully'}), 201

# Get all vehicles (auth required)
@vehicule_bp.route('', methods=['GET'])
@jwt_required()
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'id': v.id,
        'registrationNumber': v.registrationNumber,
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'rentalPrice': v.rentalPrice
    } for v in vehicles])

# Update a vehicle by ID (admin only)
@vehicule_bp.route('/<int:vehicle_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.get_json()
    vehicle.registrationNumber = data.get('registrationNumber', vehicle.registrationNumber)
    vehicle.make = data.get('make', vehicle.make)
    vehicle.model = data.get('model', vehicle.model)
    vehicle.year = data.get('year', vehicle.year)
    vehicle.rentalPrice = data.get('rentalPrice', vehicle.rentalPrice)
    db.session.commit()
    return jsonify({'message': 'Vehicle updated successfully'})

# Delete a vehicle by ID (admin only)
@vehicule_bp.route('/<int:vehicle_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
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
@vehicule_bp.route('/search/price/<string:price>', methods=['GET'])
@jwt_required()
def search_by_price(price):
    try:
        price = float(price)
    except ValueError:
        return jsonify({'message': 'Invalid price format'}), 400
    vehicles = Vehicle.query.filter(Vehicle.rentalPrice <= price).all()
    return jsonify([{
        'id': v.id,
        'registrationNumber': v.registrationNumber,
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'rentalPrice': v.rentalPrice
    } for v in vehicles])
# Search by make (auth required)
@vehicule_bp.route('/search/make/<string:make>', methods=['GET'])
@jwt_required()
def search_by_make(make):
    vehicles = Vehicle.query.filter(Vehicle.make.ilike(f'%{make}%')).all()
    if not vehicles:
        return jsonify({'message': 'No vehicles found for this make'}), 404
    return jsonify([{
        'id': v.id,
        'registrationNumber': v.registrationNumber,
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'rentalPrice': v.rentalPrice
    } for v in vehicles])

# Search by model (auth required)
@vehicule_bp.route('/search/model/<string:model>', methods=['GET'])
@jwt_required()
def search_by_model(model):
    vehicles = Vehicle.query.filter(Vehicle.model.ilike(f'%{model}%')).all()
    if not vehicles:
        return jsonify({'message': 'No vehicles found for this model'}), 404
    return jsonify([{
        'id': v.id,
        'registrationNumber': v.registrationNumber,
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'rentalPrice': v.rentalPrice
    } for v in vehicles])
# Search by year (auth required)
@vehicule_bp.route('/search/year/<int:year>', methods=['GET'])
@jwt_required()
def search_by_year(year):
    vehicles = Vehicle.query.filter(Vehicle.year == year).all()
    if not vehicles:
        return jsonify({'message': 'No vehicles found for this year'}), 404
    return jsonify([{
        'id': v.id,
        'registrationNumber': v.registrationNumber,
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'rentalPrice': v.rentalPrice
    } for v in vehicles])


