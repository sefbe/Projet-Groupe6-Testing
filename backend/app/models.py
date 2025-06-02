from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    rental_price = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "registration_number": self.registration_number,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "rental_price": self.rental_price
        }
