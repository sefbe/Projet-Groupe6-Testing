from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # ← Ajouté
import logging

from app.config import Config, TestingConfig
from flask import Flask, jsonify
from flask_jwt_extended.exceptions import JWTExtendedException

app = Flask(__name__)

# ... ta configuration JWT, db, blueprints etc.

@app.errorhandler(JWTExtendedException)
def handle_jwt_errors(e):
    return jsonify({"error": str(e)}), 422
    
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name=None):
    app = Flask(__name__)

    # Activer les CORS pour permettre les requêtes JS → API
    CORS(app)

    # Configuration
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    # Initialisation des extensions
    db.init_app(app)
    jwt.init_app(app)

    # Enregistrement des blueprints
    from app.routes.user_routes import user_bp
    from app.routes.vehicule_routes import vehicule_bp
    from app.routes.frontend_routes import frontend
    
    app.register_blueprint(user_bp)
    app.register_blueprint(vehicule_bp)
    app.register_blueprint(frontend)

    # Création des tables si besoin
    with app.app_context():
        db.create_all()

    # Gestion des erreurs JWT
    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        print(f"[JWT ERROR] Invalid token: {reason}")
        return jsonify({"msg": reason}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print("[JWT ERROR] Token expired")
        return jsonify({"msg": "Token expired"}), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        print(f"[JWT ERROR] Unauthorized: {reason}")
        return jsonify({"msg": reason}), 401

    # Logger pour le débogage
    logging.basicConfig(level=logging.DEBUG)
    

    return app

