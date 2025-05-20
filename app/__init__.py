from flask import Flask
from .models.vehicle import db  # Importez db depuis models

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicles.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from .routes.vehicle_routes import vehicle_bp
    app.register_blueprint(vehicle_bp)
    
    return app