from flask import Blueprint, request, jsonify
from app.models.user import User, db # Assurez-vous que votre modèle User est correctement importé
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)

user_bp = Blueprint("user", __name__, url_prefix="/users")
# Si vous avez un blueprint séparé pour les véhicules, assurez-vous qu'il est défini et importé ailleurs.
# Sinon, les routes spécifiques aux véhicules devraient être dans leur propre fichier de routes ou un blueprint 'vehicule_bp'.

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Champs manquants"}), 400

    if User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first():
        return jsonify({"error": "Utilisateur ou email deja existant"}), 400

    # Si 'role' est passé, utilisez-le, sinon 'user' par défaut
    role = data.get("role", "user") # Assurez-vous que 'role' peut être défini si nécessaire
    user = User(username=data["username"], email=data["email"], role=role)
    user.set_password(data["password"])
    
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Utilisateur cree avec succes"}), 201

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()

    if user and user.check_password(data.get("password")):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    return jsonify({"error": "Identifiants invalides"}), 401

@user_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    return jsonify({"access_token": access_token}), 200

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if user:
        return jsonify(user.to_dict()) # Assurez-vous que User a une méthode to_dict()
    return jsonify({"error": "Utilisateur non trouve"}), 404

@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouve"}), 404

    current_id = int(get_jwt_identity())
    # Un utilisateur non admin ne devrait pouvoir modifier que son propre profil
    # Un admin pourrait modifier d'autres profils
    # Cette logique doit être implémentée en fonction de vos besoins en rôles
    # Pour l'instant, on se base sur l'ID de l'utilisateur connecté
    #if current_id != user_id:
        # Optionnel: Si l'utilisateur a un rôle admin, il peut modifier d'autres utilisateurs
        # user_role = User.query.get(current_id).role
        # if user_role != 'admin':
        #return jsonify({"error": "Acces non autorise"}), 403


    data = request.get_json() or {}

    email = data.get("email")
    if email and "@" not in email:
        return jsonify({"error": "Email invalide"}), 400

    user.username = data.get("username", user.username)
    user.email = email or user.email
    if "password" in data:
        user.set_password(data["password"])
    if "role" in data: # Permettre la modification du rôle si l'utilisateur est admin
        user.role = data["role"]

    db.session.commit()
    return jsonify({"message": "Utilisateur mis a jour"}), 200
    
    
# Get all Users (auth required)
@user_bp.route('', methods=['GET']) # <-- Correction 1: Utilisation de user_bp et route vide
@jwt_required()
def get_users():
    users_from_db = User.query.all() # <-- Correction 2: Utilisation de User.query.all()
    user_list = [{
        'id': v.id,
        'username': v.username,
        'email': v.email,
        'role': v.role,
    } for v in users_from_db] # <-- Correction 3: Itération sur la bonne variable
    return jsonify({'users': user_list}), 200
    
    
# Delete a user by ID (admin only)
@user_bp.route('/<int:user_id>', methods=['DELETE']) # <-- Correction 4: Utilisation de user_bp et paramètre user_id
@jwt_required()
def delete_user(user_id): # <-- Correction 5: Nom de la fonction cohérent avec l'action
    # Optionnel: Ajouter une vérification de rôle admin ici
    # current_user_id = get_jwt_identity()
    # current_user = User.query.get(int(current_user_id))
    # if not current_user or current_user.role != 'admin':
    #     return jsonify({"error": "Accès non autorisé. Rôle admin requis."}), 403

    user_to_delete = User.query.get(user_id) # <-- Correction 6: Utilisation de User.query.get()
    if user_to_delete is None:
        return jsonify({"message": "Utilisateur non trouve"}), 404
    
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200 # Statut 200 ou 204 No Content


def get_user_by_id(user_id, return_json=False):
    """
    Récupère un utilisateur à partir de son ID avec vérification et gestion d'erreur.

    Args:
        user_id (int | str): L'identifiant de l'utilisateur
        return_json (bool): Si True, retourne un jsonify dict, sinon un objet User ou None

    Returns:
        User | (Response, int): L'utilisateur ou un tuple (json, code)
    """
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        if return_json:
            return jsonify({"error": "ID utilisateur invalide"}), 400
        return None

    user = User.query.get(user_id)

    if not user:
        if return_json:
            return jsonify({"error": "Utilisateur non trouvé"}), 404
        return None

    if return_json:
        return jsonify(user.to_dict()), 200

    return user

