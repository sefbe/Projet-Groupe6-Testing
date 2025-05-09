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

    # Import du modèle
    from app.models import vehicule

    # Import et enregistrement des routes
    from app.routes.vehicule_routes import vehicule_bp
    app.register_blueprint(vehicule_bp, url_prefix='/api/vehicles')

    return app

