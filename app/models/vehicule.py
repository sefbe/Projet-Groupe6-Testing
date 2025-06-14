from flask_sqlalchemy import SQLAlchemy
from app.models import db

#db = SQLAlchemy()

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    registrationNumber = db.Column(db.String(100), unique=True, nullable=False)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rentalPrice = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Vehicle {self.registrationNumber}>"

