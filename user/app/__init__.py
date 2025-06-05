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
    from app.models.user_model import User

    # Import et enregistrement des routes
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    return app