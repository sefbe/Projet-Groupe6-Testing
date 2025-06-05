from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import des modèles ici (important pour les migrations)
    from app.models import vehicle


    # Import et enregistrement des routes
    from app.routes.vehicle_routes import vehicle_bp
    app.register_blueprint(vehicle_bp)

    return app

