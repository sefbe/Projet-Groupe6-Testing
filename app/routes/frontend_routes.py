from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def home():
    return render_template('login.html')

@frontend.route('/register')
def register():
    return render_template('register.html')

@frontend.route('/vehicle')
def vehicles():
    return render_template('vehicles.html')


# Détails ou édition d’un véhicule spécifique (admin)
@frontend.route('/vehicles/<int:vehicle_id>/edit')
def edit_vehicle(vehicle_id):
    return render_template('edit_vehicle.html', vehicle_id=vehicle_id)

# Profil de l'utilisateur connecté
@frontend.route('/profile')
def profile():
    return render_template('profile.html')

