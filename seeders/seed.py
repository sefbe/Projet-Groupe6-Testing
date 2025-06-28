import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db, create_app
from app.models.user import User
from app.models.vehicule import Vehicle
from werkzeug.security import generate_password_hash

app = create_app()

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Créer des utilisateurs
        user1 = User(username="admin", email="admin@example.com", role="admin")
        user1.set_password("admin123")
        user2 = User(username="john", email="john@example.com", role="user")
        user2.set_password("pass456")

        # Créer des véhicules
        vehicle1 = Vehicle(
            registrationNumber="AA-111-AA",
            make="Peugeot",
            model="208",
            year=2021,
            rentalPrice=45.0
        )
        vehicle2 = Vehicle(
            registrationNumber="BB-222-BB",
            make="Renault",
            model="Clio",
            year=2020,
            rentalPrice=40.0
        )

        db.session.add_all([user1, user2, vehicle1, vehicle2])
        db.session.commit()
        print("Données seedées avec succès.")

if __name__ == "__main__":
    seed()
