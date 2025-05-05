from flask import Blueprint, request, jsonify
from app.models.vehicule import db, Vehicle

vehicule_bp = Blueprint('vehicule_bp', __name__, url_prefix='/vehicles')

# Create a vehicle
@vehicule_bp.route('', methods=['POST'])
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

# Get all vehicles
@vehicule_bp.route('', methods=['GET'])
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

# Update a vehicle by ID
@vehicule_bp.route('/<int:vehicle_id>', methods=['PUT'])
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

# Delete a vehicle by ID
@vehicule_bp.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle deleted successfully'})

# Search by registration number
@vehicule_bp.route('/search/registration/<string:registration_number>', methods=['GET'])
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

# Search by rental price (vehicles <= price)
@vehicule_bp.route('/search/price/<float:price>', methods=['GET'])
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

