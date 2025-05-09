import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # Connexion à une base de données MySQL avec PyMySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://username:password@localhost:3306/vehicles_db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

