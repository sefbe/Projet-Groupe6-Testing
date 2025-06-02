from .models import Vehicle, db
from sqlalchemy.exc import IntegrityError


def validate_vehicle_data(data, required=True):
    fields = ["registration_number", "make", "model", "year", "rental_price"]
    if required:
        for field in fields:
            if field not in data:
                raise KeyError(f"Missing field: {field}")

    if "year" in data and not isinstance(data["year"], int):
        raise ValueError("Year must be an integer")

    if "rental_price" in data and not isinstance(data["rental_price"], (int, float)):
        raise ValueError("Rental price must be a number")


def create_vehicle(data):
    validate_vehicle_data(data)
    vehicle = Vehicle(
        registration_number=data["registration_number"],
        make=data["make"],
        model=data["model"],
        year=int(data["year"]),
        rental_price=float(data["rental_price"])
    )
    db.session.add(vehicle)
    try:
        db.session.commit()
        return vehicle
    except IntegrityError:
        db.session.rollback()
        return None  # Or return {"error": "duplicate"}


def get_all_vehicles():
    return Vehicle.query.all()


def get_vehicle_by_id(vehicle_id):
    return Vehicle.query.get(vehicle_id)


def find_by_registration_number(reg_number):
    return Vehicle.query.filter_by(registration_number=reg_number).first()


def find_by_price(price):
    return Vehicle.query.filter_by(rental_price=price).all()


def update_vehicle(vehicle_id, data):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return None

    validate_vehicle_data(data, required=False)

    for key, value in data.items():
        if hasattr(vehicle, key):
            setattr(vehicle, key, value)
    db.session.commit()
    return vehicle


def delete_vehicle(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if not vehicle:
        return False
    db.session.delete(vehicle)
    db.session.commit()
    return True
