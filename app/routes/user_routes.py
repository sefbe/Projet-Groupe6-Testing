from flask import Blueprint, request, jsonify
from app.models.user import User, db
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Champs manquants"}), 400

    if User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first():
        return jsonify({"error": "Utilisateur ou email déjà existant"}), 400
    if "role" in data and data["role"] not in ["user", "admin"]:
        return jsonify({"error": "Rôle invalide"}), 400
    if "role" in data:
        user = User(username=data["username"], email=data["email"], role=data["role"])
    else:
        user = User(username=data["username"], email=data["email"])

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
    access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": access_token}), 200

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "Utilisateur non trouvé"}), 404

@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    current_id = get_jwt_identity()
    if int(current_id) != user_id:
        return jsonify({"error": "Accès non autorisé"}), 403

    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    if "password" in data:
        user.set_password(data["password"])

    db.session.commit()
    return jsonify({"message": "Utilisateur mis à jour"}), 200

