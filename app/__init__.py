from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from tenacity import retry, stop_after_attempt, wait_fixed
import logging

from app.config import Config, TestingConfig
from flask_jwt_extended.exceptions import JWTExtendedException

db = SQLAlchemy()
jwt = JWTManager()

@retry(stop=stop_after_attempt(10), wait=wait_fixed(5))
def init_db(app):
    if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
        logging.debug("Initializing SQLAlchemy for app")
        db.init_app(app)
        
        # IMPORTANT: Import all models to register them with SQLAlchemy
        from app.models import User, Vehicle
        
        with app.app_context():
            logging.debug("Creating all tables")
            db.create_all()
            # Vérifier les tables créées
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            logging.debug(f"Tables in database: {tables}")

def create_app(config_name=None):
    app = Flask(__name__)

    CORS(app)

    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    init_db(app)
    jwt.init_app(app)

    from app.routes.user_routes import user_bp
    from app.routes.vehicule_routes import vehicule_bp
    from app.routes.frontend_routes import frontend

    app.register_blueprint(user_bp)
    app.register_blueprint(vehicule_bp)
    app.register_blueprint(frontend)

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

    @app.errorhandler(JWTExtendedException)
    def handle_jwt_errors(e):
        return jsonify({"error": str(e)}), 422

    logging.basicConfig(level=logging.DEBUG)
    return app