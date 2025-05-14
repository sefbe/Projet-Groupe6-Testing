from app import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(50), unique=True, nullable=False)
    rental_price = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'make': self.brand,
            'model': self.model,
            'registration_number': self.registration_number,
            'rental_price': self.rental_price,
            'year': self.year,
            'available': self.available
        }

    def __repr__(self):
        return f'<Vehicle {self.registration_number}>'

