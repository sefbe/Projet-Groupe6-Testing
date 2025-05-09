import pytest
from app import create_app, db
from app.models.vehicule import Vehicle



def test_create_vehicle(client, new_vehicle):
    # Arrange
    vehicle_data = {
        'registrationNumber': new_vehicle.registrationNumber,
        'make': new_vehicle.make,
        'model': new_vehicle.model,
        'year': new_vehicle.year,
        'rentalPrice': new_vehicle.rentalPrice
    }
    
    # Act
    response = client.post('api/vehicles', json=vehicle_data)
    
    # Assert
    assert response.status_code == 201
    assert b'Vehicle created successfully' in response.data


def test_get_vehicles(client, new_vehicle):
    # Arrange
    db.session.add(new_vehicle)
    db.session.commit()
    
    # Act
    response = client.get('api/vehicles')
    
    # Assert
    assert response.status_code == 200
    assert b'Toyota' in response.data  # Vérifie que la marque du véhicule est présente dans la réponse

"""
def test_update_vehicle(client, new_vehicle):
    # Arrange
    db.session.add(new_vehicle)
    db.session.commit()
    
    updated_data = {
        'registrationNumber': 'XYZ456',
        'make': 'Honda',
        'model': 'Civic',
        'year': 2021,
        'rentalPrice': 55.0
    }
    
    # Act
    response = client.put(f'api/vehicles/{new_vehicle.id}', json=updated_data)
    
    # Assert
    assert response.status_code == 200
    assert b'Vehicle updated successfully' in response.data
    
    # Vérifier que les données ont été mises à jour dans la base de données
    updated_vehicle = Vehicle.query.get(new_vehicle.id)
    assert updated_vehicle.make == 'Honda'


def test_delete_vehicle(client, new_vehicle):
    # Arrange
    db.session.add(new_vehicle)
    db.session.commit()
    
    # Act
    response = client.delete(f'api/vehicles/{new_vehicle.id}')
    
    # Assert
    assert response.status_code == 200
    assert b'Vehicle deleted successfully' in response.data
    
    # Vérifier que le véhicule a bien été supprimé de la base de données
    deleted_vehicle = Vehicle.query.get(new_vehicle.id)
    assert deleted_vehicle is None
"""

def test_search_by_registration(client, new_vehicle):
    # Arrange
    db.session.add(new_vehicle)
    db.session.commit()
    
    # Act
    response = client.get(f'api/vehicles/search/registration/{new_vehicle.registrationNumber}')
    
    # Assert
    assert response.status_code == 200
    assert b'Toyota' in response.data  # Vérifie que le véhicule a bien été retrouvé


def test_search_by_price(client, new_vehicle):
    # Arrange
    db.session.add(new_vehicle)
    db.session.commit()
    
    # Act
    response = client.get('api/vehicles/search/price/60.0')  # Recherche tous les véhicules <= 60
    
    # Assert
    assert response.status_code == 200
    assert b'Toyota' in response.data  # Vérifie que le véhicule est dans les résultats de la recherche


def test_search_by_price_no_results(client, new_vehicle):
    # Arrange
    db.session.add(new_vehicle)
    db.session.commit()
    
    # Act
    response = client.get('api/vehicles/search/price/40.0')  # Recherche les véhicules <= 40 (aucun résultat)
    
    # Assert
    assert response.status_code == 200
    assert b'[]' in response.data  # Aucun véhicule ne doit être trouvé

