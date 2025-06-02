from .models import Vehicle, db

def create_vehicle(data):
    vehicle = Vehicle(
        registration_number=data["registration_number"],
        make=data["make"],
        model=data["model"],
        year=data["year"],
        rental_price=data["rental_price"],
    )
    db.session.add(vehicle)
    db.session.commit()
    return vehicle

def get_all_vehicles():
    return Vehicle.query.all()

def get_vehicle_by_id(vehicle_id):
    return Vehicle.query.get(vehicle_id)

def update_vehicle(vehicle_id, data):
    vehicle = Vehicle.query.get(vehicle_id)
    for key, value in data.items():
        setattr(vehicle, key, value)
    db.session.commit()
    return vehicle

def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()

def find_by_registration_number(reg_number):
    return Vehicle.query.filter_by(registration_number=reg_number).first()

def find_by_price(price):
    return Vehicle.query.filter_by(rental_price=price).all()
