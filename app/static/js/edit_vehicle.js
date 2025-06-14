const token = localStorage.getItem('access_token');
const BASE_URL = 'http://localhost:5000'; // Remplace si nécessaire par l'URL de ton backend

// Affiche un message (erreur ou succès)
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

    setTimeout(() => {
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
    }, 3000);
}

document.addEventListener('DOMContentLoaded', async () => {
    // Vérifie le token
    if (!token) {
        displayMessage('error', "Session expirée. Veuillez vous reconnecter.");
        setTimeout(() => { window.location.href = "/"; }, 2000);
        return;
    }

    // Récupère l'ID du véhicule depuis l'URL
    const pathSegments = window.location.pathname.split('/');
    const vehicleId = pathSegments[pathSegments.length - 2];

    if (!vehicleId || isNaN(vehicleId)) {
        displayMessage('error', "ID de véhicule invalide ou manquant dans l'URL.");
        setTimeout(() => { window.location.href = '/vehicle'; }, 2000);
        return;
    }

    document.getElementById('vehicleId').value = vehicleId;
    await loadVehicleData(vehicleId);

    const editVehicleForm = document.getElementById('editVehicleForm');

    editVehicleForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(editVehicleForm);
        const data = Object.fromEntries(formData.entries());

        // Conversion des champs numériques
        data.year = parseInt(data.year);
        data.rental_price = parseFloat(data.rental_price);

        try {
            const res = await fetch(`${BASE_URL}/vehicles/${vehicleId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify(data)
            });

            if (!res.ok) {
                const errorData = await res.json();
                displayMessage('error', errorData.error || "Échec de la modification du véhicule.");
                return;
            }

            displayMessage('success', "Véhicule modifié avec succès ! Redirection...");
            setTimeout(() => {
                window.location.href = '/vehicle';
            }, 1500);

        } catch (error) {
            console.error('Erreur lors de la requête PUT :', error);
            displayMessage('error', "Erreur réseau ou serveur.");
        }
    });
});

// Charge les données du véhicule pour pré-remplir le formulaire
async function loadVehicleData(id) {
    try {
        const res = await fetch(`${BASE_URL}/vehicles/${id}`, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        console.log(id);
        console.log(res);

        if (!res.ok) {
            const errorData = await res.json();
            displayMessage('error', errorData.error || "Impossible de charger les données du véhicule.");
            setTimeout(() => { window.location.href = '/vehicle'; }, 2000);
            return;
        }

	const data = await res.json();
	const vehicle = data.vehicle;

	document.getElementById('registrationNumber').value = vehicle.registrationNumber || '';
	document.getElementById('make').value = vehicle.make || '';
	document.getElementById('model').value = vehicle.model || '';
	document.getElementById('year').value = vehicle.year || 2000;
	document.getElementById('rentalPrice').value = vehicle.rentalPrice || 0;


    } catch (error) {
        console.error('Erreur lors du chargement des données du véhicule :', error);
        displayMessage('error', "Erreur réseau ou serveur.");
        setTimeout(() => { window.location.href = '/vehicle'; }, 2000);
    }
}

