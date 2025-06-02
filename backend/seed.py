from app import create_app, db
from app.models import Vehicle

app = create_app()

with app.app_context():
    db.create_all()

    # Données fictives
    vehicles = [
        Vehicle(
            registration_number="SEED001",
            make="Toyota",
            model="Corolla",
            year=2018,
            rental_price=60.0
        ),
        Vehicle(
            registration_number="SEED002",
            make="Honda",
            model="Civic",
            year=2020,
            rental_price=75.5
        ),
        Vehicle(
            registration_number="SEED003",
            make="Tesla",
            model="Model 3",
            year=2023,
            rental_price=150.0
        )
    ]

    db.session.bulk_save_objects(vehicles)
    db.session.commit()
    print("✔️ Base de données initialisée avec 3 véhicules")
