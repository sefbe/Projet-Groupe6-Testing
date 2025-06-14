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
#@jwt_required() # Assurez-vous que l'accès au tableau de bord des véhicules nécessite une authentification
def vehicles():
    return render_template('vehicles.html')

# Nouvelle route pour la page d'ajout d'un véhicule
@frontend.route('/add_vehicle')
#@jwt_required() # Il est fortement recommandé de protéger cette route avec une authentification
def add_vehicle():
    return render_template('add_vehicle.html')


# Détails ou édition d’un véhicule spécifique (admin)
@frontend.route('/vehicles/<int:vehicle_id>/edit')
#@jwt_required() # Protéger également cette route
def edit_vehicle(vehicle_id):
    return render_template('edit_vehicle.html', vehicle_id=vehicle_id)

@frontend.route('/user')
#@jwt_required()
def list_users():
    return render_template('users.html')

@frontend.route('/add')
#@jwt_required()
def add_user():
    return render_template('add_users.html')

from .user_routes import get_user_by_id

@frontend.route("/edit/<int:user_id>")
def edit_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return "Utilisateur non trouvé", 404
    return render_template("edit_users.html", user=user)

    
# Profil de l'utilisateur connecté
@frontend.route('/profile')
#@jwt_required() # Protéger cette route
def profile():
    return render_template('profile.html')
