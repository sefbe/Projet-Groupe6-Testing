import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # Connexion à une base de données MySQL avec PyMySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root@localhost:3306/vehicles_db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False



class ConfigTest:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
    JWT_SECRET_KEY = 'jwt-test-secret'
    WTF_CSRF_ENABLED = False

