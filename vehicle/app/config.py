import os
from dotenv import load_dotenv

# Charge les variables depuis .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL n'est pas défini dans l'environnement ou le fichier .env")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

