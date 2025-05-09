import pytest
from app import create_app, db
from app.models.vehicule import Vehicle

@pytest.fixture
def app_instance():
    app = create_app()
    app.config['TESTING'] = True
    
    # Remplace cette ligne par la configuration MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ronel@localhost/vehicule_test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Crée les tables dans la base de données MySQL
        yield app
        db.session.remove()
        db.drop_all()  # Supprime les tables après les tests

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

@pytest.fixture
def new_vehicle():
    return Vehicle(
        registrationNumber='ABC123',
        make='Toyota',
        model='Corolla',
        year=2020,
        rentalPrice=50.0
    )

