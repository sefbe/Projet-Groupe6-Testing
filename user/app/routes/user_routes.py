from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.services.auth_service import AuthService

user_bp = Blueprint("user", __name__)

@user_bp.route("/user", methods=["POST"])
def create_user():
    """
    Crée un utilisateur avec un rôle par défaut "user".
    Accessible via la route /user.
    """
    data = request.json
    user_id = UserService.create_user(data["name"], data["email"], data["password"], role="user")
    return jsonify({"id": user_id}), 201

@user_bp.route("/users", methods=["GET"])
def get_users():
    """
    Récupère tous les utilisateurs.
    Accessible via la route /users.
    """
    users = UserService.get_users()
    return jsonify(users), 200

@user_bp.route("/login", methods=["POST"])
def login():
    """
    Authentifie un utilisateur et génère des tokens JWT.
    """
    data = request.json
    user = UserService.get_user_by_email(data["email"])
    if user and AuthService.verify_password(data["password"], user["password"]):  # Vérification sécurisée du mot de passe
        access_token = AuthService.generate_access_token(user["id"], user["role"])  # Inclure le rôle dans le token
        refresh_token = AuthService.generate_refresh_token(user["id"])
        return jsonify({"access_token": access_token, "refresh_token": refresh_token, "role": user["role"]}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Met à jour les informations d'un utilisateur.
    """
    data = request.json
    rows_affected = UserService.update_user(user_id, data["name"], data["email"], data["password"])
    if rows_affected:
        return jsonify({"message": "User updated"}), 200
    return jsonify({"message": "User not found"}), 404

@user_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """
    Génère un nouveau token d'accès à partir d'un token de rafraîchissement.
    """
    refresh_token = request.headers.get("Authorization")
    payload = AuthService.decode_token(refresh_token)
    if payload:
        new_access_token = AuthService.generate_access_token(payload["user_id"], payload["role"])  # Inclure le rôle
        return jsonify({"access_token": new_access_token}), 200
    return jsonify({"message": "Invalid or expired refresh token"}), 401