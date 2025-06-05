from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests

frontend_bp = Blueprint("frontend", __name__)

USER_API_URL = "http://127.0.0.1:5002"
VEHICLE_API_URL = "http://127.0.0.1:5001"

@frontend_bp.route("/")
def home():
    return render_template("index.html")

@frontend_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        response = requests.post(f"{USER_API_URL}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            tokens = response.json()
            session["access_token"] = tokens["access_token"]
            session["refresh_token"] = tokens["refresh_token"]
            session["role"] = tokens["role"] # Default to 'user' if role not provided
            return render_template("index.html")
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@frontend_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        response = requests.post(f"{USER_API_URL}/user", json={"name": name, "email": email, "password": password})
        if response.status_code == 201:
            flash("User registered successfully", "success")
            return redirect(url_for("frontend.login"))
        flash("Registration failed", "danger")
    return render_template("register.html")

@frontend_bp.route("/users")
def get_users():
    """
    Récupère tous les utilisateurs et les affiche (admin uniquement).
    """
    access_token = session.get("access_token")
    if not access_token or session.get("role") != "admin":
        return redirect(url_for("frontend.login"))
    response = requests.get(f"{USER_API_URL}/users", headers={"Authorization": access_token})
    if response.status_code == 200:
        users = response.json()
        return render_template("users.html", users=users)
    flash("Failed to fetch users", "danger")
    return redirect(url_for("frontend.home"))

@frontend_bp.route("/vehicles")
def vehicles():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("frontend.login"))
    response = requests.get(f"{VEHICLE_API_URL}/vehicles", headers={"Authorization": access_token})
    if response.status_code == 200:
        vehicles = response.json()
        return render_template("vehicles.html", vehicles=vehicles)
    flash("Failed to fetch vehicles", "danger")
    return redirect(url_for("frontend.login"))

@frontend_bp.route("/vehicle/create", methods=["GET", "POST"])
def create_vehicle():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("frontend.login"))
    if request.method == "POST":
        data = {
            "make": request.form["make"],
            "model": request.form["model"],
            "registration_number": request.form["registration_number"],
            "rental_price": request.form["rental_price"],
            "year": request.form["year"],
            "available": request.form.get("available") == "on"
        }
        response = requests.post(f"{VEHICLE_API_URL}/vehicle/create", json=data, headers={"Authorization": access_token})
        if response.status_code == 201:
            flash("Vehicle created successfully", "success")
            return redirect(url_for("frontend.vehicles"))
        flash("Failed to create vehicle", "danger")
    return render_template("create_vehicle.html")

@frontend_bp.route("/vehicle/update/<int:id>", methods=["GET", "POST"])
def update_vehicle(id):
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("frontend.login"))
    if request.method == "POST":
        data = {
            "make": request.form["make"],
            "model": request.form["model"],
            "registration_number": request.form["registration_number"],
            "rental_price": request.form["rental_price"],
            "year": request.form["year"],
            "available": request.form.get("available") == "on"
        }
        response = requests.put(f"{VEHICLE_API_URL}/vehicle/update/{id}", json=data, headers={"Authorization": access_token})
        if response.status_code == 200:
            flash("Vehicle updated successfully", "success")
            return redirect(url_for("frontend.vehicles"))
        flash("Failed to update vehicle", "danger")
    response = requests.get(f"{VEHICLE_API_URL}/vehicle/{id}", headers={"Authorization": access_token})
    if response.status_code == 200:
        vehicle = response.json()
        return render_template("update_vehicle.html", vehicle=vehicle)
    flash("Failed to fetch vehicle details", "danger")
    return redirect(url_for("frontend.vehicles"))

@frontend_bp.route("/search", methods=["POST"])
def search():
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("frontend.login"))

    query = request.form["query"]
    if query.isdigit():  # Si la saisie est un nombre, recherche par prix maximum
        response = requests.get(f"{VEHICLE_API_URL}/vehicles/price/{query}", headers={"Authorization": access_token})
    else:  # Sinon, recherche par numéro d'immatriculation
        response = requests.get(f"{VEHICLE_API_URL}/vehicle/search/{query}", headers={"Authorization": access_token})

    if response.status_code == 200:
        vehicles = response.json()
        return render_template("search_results.html", vehicles=vehicles)
    flash("No results found", "danger")
    return redirect(url_for("frontend.vehicles"))

@frontend_bp.route("/logout")
def logout():
    session.pop("access_token", None)
    session.pop("refresh_token", None)
    flash("You have been logged out", "success")
    return redirect(url_for("frontend.home"))

@frontend_bp.route("/user/update/<int:id>", methods=["GET", "POST"])
def update_user(id):
    """
    Permet à un utilisateur de mettre à jour ses informations.
    """
    access_token = session.get("access_token")
    if not access_token:
        return redirect(url_for("frontend.login"))
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"]
        }
        response = requests.put(f"{USER_API_URL}/users/{id}", json=data, headers={"Authorization": access_token})
        if response.status_code == 200:
            flash("User updated successfully", "success")
            return redirect(url_for("frontend.home"))
        flash("Failed to update user", "danger")
    response = requests.get(f"{USER_API_URL}/users/{id}", headers={"Authorization": access_token})
    if response.status_code == 200:
        user = response.json()
        return render_template("update_user.html", user=user)
    flash("Failed to fetch user details", "danger")
    return redirect(url_for("frontend.home"))