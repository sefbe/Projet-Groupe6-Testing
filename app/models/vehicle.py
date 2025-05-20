from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Déclaration locale de db

class Vehicle(db.Model):
    tablename = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    registrationNumber = db.Column(db.String(100), unique=True, nullable=False)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rentalPrice = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "registrationNumber": self.registrationNumber,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "rentalPrice": self.rentalPrice
        }