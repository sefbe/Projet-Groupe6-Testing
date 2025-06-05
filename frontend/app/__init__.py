from flask import Flask
from app.routes.frontend_routes import frontend_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "oursecretkeyGroupe6"
    app.register_blueprint(frontend_bp)
    return app