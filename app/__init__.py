from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .config import ConfigTest
from flask_jwt_extended import JWTManager as JWT
db = SQLAlchemy()
migrate = Migrate()
jwt= JWT()
def create_app(config_name=None):
    app = Flask(__name__)
    if config_name == 'testing':
        app.config.from_object(ConfigTest)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import du modèle
    from app.models import vehicule

    # Import et enregistrement des routes
    from app.routes.vehicule_routes import vehicule_bp
    app.register_blueprint(vehicule_bp, url_prefix='/api/vehicles')

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    


    return app

