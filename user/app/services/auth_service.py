import jwt
import datetime
from app.config import Config
from werkzeug.security import check_password_hash, generate_password_hash

class AuthService:
    @staticmethod
    def generate_access_token(user_id, role):
        """
        Génère un token d'accès JWT avec l'ID utilisateur et le rôle.
        """
        payload = {
            "user_id": user_id,
            "role": role,  # Inclure le rôle dans le token
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def generate_refresh_token(user_id):
        """
        Génère un token de rafraîchissement JWT.
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS)
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_token(token):
        """
        Décode un token JWT et retourne son payload.
        """
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            return payload  # Retourne tout le payload (inclut user_id et role)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Vérifie si un mot de passe en clair correspond à son hash.
        """
        return check_password_hash(hashed_password, plain_password)

    @staticmethod
    def hash_password(password):
        """
        Génère un hash sécurisé pour un mot de passe.
        """
        return generate_password_hash(password, method="pbkdf2:sha256")  # Utiliser pbkdf2:sha256