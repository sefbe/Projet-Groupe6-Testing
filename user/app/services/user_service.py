from app.models.user_model import User
from app import db
from app.services.auth_service import AuthService

class UserService:
    @staticmethod
    def create_user(name, email, password, role="user"):
        """
        Crée un utilisateur avec un rôle par défaut "user".
        """
        hashed_password = AuthService.hash_password(password)  # Hash sécurisé du mot de passe
        user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        return user.id

    @staticmethod
    def get_user_by_email(email):
        """
        Récupère un utilisateur par son email.
        """
        user = User.query.filter_by(email=email).first()
        return user.to_dict() if user else None

    @staticmethod
    def update_user(user_id, name, email, password):
        """
        Met à jour les informations d'un utilisateur.
        """
        user = User.query.get(user_id)
        if user:
            user.name = name
            user.email = email
            user.password = AuthService.hash_password(password)  # Hash sécurisé du mot de passe
            db.session.commit()
            return 1
        return 0

    @staticmethod
    def get_users():
        """
        Récupère tous les utilisateurs.
        """
        users = User.query.all()
        return [user.to_dict() for user in users]