from app import db, create_app
from app.models.user_model import User
from app.services.auth_service import AuthService

# Créer une instance de l'application Flask
app = create_app()

# Utiliser le contexte de l'application
with app.app_context():
    # Récupérer tous les utilisateurs
    users = User.query.all()

    for user in users:
        # Vérifier si le mot de passe n'est pas déjà haché
        if not user.password.startswith("pbkdf2:sha256:"):
            print(f"Hachage du mot de passe pour l'utilisateur {user.email}")
            user.password = AuthService.hash_password(user.password)  # Hacher le mot de passe
            db.session.add(user)

    # Appliquer les modifications
    db.session.commit()
    print("Tous les mots de passe ont été mis à jour.")
