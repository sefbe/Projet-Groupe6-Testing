import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    # Connexion à une base de données MySQL avec PyMySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:ronel@localhost:3306/vehicles_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


"""
class TestingConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    # Connexion à une base de données MySQL avec PyMySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:ronel@localhost:3306/vehicles_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
"""

# configuration des tests
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Utilisation d'une base de données en mémoire pour les tests
    WTF_CSRF_ENABLED = False  # Désactive CSRF pour les tests
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Durée de vie des tokens plus courte pour les tests
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)  # Durée de vie des tokens de rafraîchissement plus courte pour les tests
# Configuration de l'application Flask
