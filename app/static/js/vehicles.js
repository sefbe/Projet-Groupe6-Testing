// static/js/vehicles.js

const token = localStorage.getItem('access_token');
const BASE_URL = 'http://localhost:5000'; // Assurez-vous que cela correspond à l'URL de votre backend Flask

// Vérification de l'authentification et redirection
if (!token) {
    displayMessage('error', "Session expirée. Veuillez vous reconnecter.");
    setTimeout(() => { window.location.href = "/"; }, 2000);
}

// Fonction pour afficher les messages (erreur/succès)
function displayMessage(type, message) {
    const errorDiv = document.getElementById('errorMessage');
    const successDiv = document.getElementById('successMessage');

    errorDiv.style.display = 'none';
    successDiv.style.display = 'none';

    if (type === 'error') {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    } else if (type === 'success') {
        successDiv.textContent = message;
        successDiv.style.display = 'block';
    }
    // Masquer le message après quelques secondes
    setTimeout(() => {
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
    }, 3000);
}

// Charger les véhicules depuis l'API backend
async function loadVehicles() {
    try {
        const res = await fetch(`${BASE_URL}/vehicles`, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (!res.ok) {
            const errorData = await res.json();
            displayMessage('error', errorData.error || "Échec du chargement des véhicules.");
            return;
        }
        const data = await res.json();
        // CORRECTION : Accédez à la clé 'vehicles' de l'objet data
        if (data && Array.isArray(data.vehicles)) {
            displayVehicles(data.vehicles);
        } else {
            // Gérer le cas où la structure de réponse est inattendue
            console.error('La réponse de l\'API pour /vehicles n\'était pas un tableau de véhicules :', data);
            displayMessage('error', "Format de données de véhicules inattendu.");
            displayVehicles([]); // Afficher une liste vide
        }
    } catch (error) {
        console.error('Erreur lors du chargement des véhicules :', error);
        displayMessage('error', "Erreur réseau ou du serveur lors du chargement des véhicules.");
    }
}

// Fonction pour afficher les véhicules dans l'interface utilisateur
function displayVehicles(vehicles) {
    const vehicleListDiv = document.getElementById('vehicle-list');
    vehicleListDiv.innerHTML = ''; // Effacer la liste actuelle

    if (!vehicles || vehicles.length === 0) { // Vérifier si nul/non défini ou tableau vide
        vehicleListDiv.innerHTML = '<p>Aucun véhicule trouvé.</p>';
        return;
    }

    // List of image paths (assuming they are in static/images and named car1.jpeg, car2.jpeg, etc.)
    const images = [
        'static/images/car1.jpeg',
        'static/images/car2.jpeg',
        'static/images/car3.jpeg',
        'static/images/car4.jpeg',
        'static/images/car5.jpeg',
        // Add more image paths here as needed
    ];

    vehicles.forEach(vehicle => {
        const vehicleCard = document.createElement('div');
        vehicleCard.className = 'vehicle-card';

        // Select a random image from the list
        const randomImage = images[Math.floor(Math.random() * images.length)];

        // Construct the HTML for each vehicle card, including the image, overlay, and separate content/actions sections
        vehicleCard.innerHTML = `
            <div class="image-container">
                <img src="${randomImage}" alt="${vehicle.make} ${vehicle.model}">
                <div class="vehicle-details-overlay">
                    <h3>${vehicle.make} ${vehicle.model} (${vehicle.year})</h3>
                    <p><strong>Matricule :</strong> ${vehicle.registrationNumber}</p>
                    <p><strong>Prix :</strong> ${vehicle.rentalPrice} FCFA</p>
                </div>
            </div>
            <div class="card-content">
                <h3>${vehicle.make} ${vehicle.model}</h3>
            </div>
            <div class="actions">
                <button onclick="editVehicle('${vehicle.id}')">Modifier</button>
                <button onclick="deleteVehicle('${vehicle.id}')">Supprimer</button>
            </div>
        `;
        vehicleListDiv.appendChild(vehicleCard);
    });
}

// Modifier un véhicule (cette fonction redirigera vers la page de modification)
function editVehicle(id) {
    window.location.href = `/vehicles/${id}/edit`; // REDIRECTION VERS LA PAGE D'ÉDITION
}

// Supprimer un véhicule
async function deleteVehicle(id) {
    if (!confirm("Êtes-vous sûr de vouloir supprimer ce véhicule ?")) return;

    try {
        const res = await fetch(`${BASE_URL}/vehicles/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': 'Bearer ' + token }
        });

        if (!res.ok) {
            const errorData = await res.json();
            displayMessage('error', errorData.error || "Échec de la suppression du véhicule.");
            return;
        }

        loadVehicles(); // Recharger la liste
        displayMessage('success', "Véhicule supprimé avec succès !");
    } catch (error) {
        console.error('Erreur lors de la suppression du véhicule :', error);
        displayMessage('error', "Erreur réseau ou du serveur lors de la suppression du véhicule.");
    }
}

// Écouteur pour le bouton "Ajouter un véhicule"
document.getElementById('add-vehicle-btn').addEventListener('click', () => {
    window.location.href = '/add_vehicle'; // REDIRECTION VERS LA PAGE D'AJOUT
});


// Filtrer les véhicules par numéro d'immatriculation
async function filterByRegistration() {
    const registrationNumber = document.getElementById('filter-registration').value;
    if (!registrationNumber) {
        displayMessage('error', "Veuillez entrer un numéro d'immatriculation pour filtrer.");
        loadVehicles(); // Recharger tous les véhicules si le filtre est vide
        return;
    }
    try {
        const res = await fetch(`${BASE_URL}/vehicles/search/registration/${registrationNumber}`, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (!res.ok) {
            const errorData = await res.json();
            displayMessage('error', errorData.error || "Erreur lors de la recherche par immatriculation.");
            return;
        }
        const data = await res.json();
        displayVehicles([data]); // Encapsuler un objet unique dans un tableau pour l'affichage
    } catch (error) {
        console.error('Erreur lors du filtrage par immatriculation :', error);
        displayMessage('error', "Erreur réseau ou du serveur lors de la recherche par immatriculation.");
    }
}

// Filtrer les véhicules par prix maximum
async function filterByPrice() {
    const price = document.getElementById('filter-price').value;
    if (!price) {
        loadVehicles();
        return;
    }
    const floatPrice = parseFloat(price).toFixed(1);
    try {
        const res = await fetch(`${BASE_URL}/vehicles/search/price/${floatPrice}`, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (!res.ok) {
            const errorData = await res.json();
            displayMessage('error', errorData.error || "Erreur lors de la recherche par prix.");
            return;
        }
        const data = await res.json();
        displayVehicles(data);
    } catch (error) {
        console.error('Erreur lors du filtrage par prix :', error);
        displayMessage('error', "Erreur réseau ou du serveur lors de la recherche par prix.");
    }
}


// Écouteur d'événements pour le bouton "Gérer les utilisateurs"
document.getElementById('go-to-users').addEventListener('click', () => {
    window.location.href = '/user'; // Navigue vers la page de gestion des utilisateurs
});


// Charger les véhicules au chargement de la page
document.addEventListener('DOMContentLoaded', loadVehicles);
