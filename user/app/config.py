import os
from dotenv import load_dotenv
load_dotenv()



class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "userSecretKey123")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:311937Sefa%40@localhost/users"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

#f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:{os.getenv('MYSQL_PASSWORD', '311937Sefa@')}@{os.getenv('MYSQL_HOST', 'localhost')}:{os.getenv('MYSQL_PORT', 3306)}/{os.getenv('MYSQL_DB', 'users')}"
