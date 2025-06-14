const token = localStorage.getItem('access_token');
const BASE_URL = 'http://localhost:5000'; // Assurez-vous que cela correspond bien à votre backend Flask

// Vérification de l'authentification
if (!token) {
    displayMessage('error', "Session expirée. Veuillez vous reconnecter.");
    setTimeout(() => { window.location.href = "/"; }, 2000);
}

// Fonction pour afficher les messages d'erreur ou de succès
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

    // Masquer les messages après 3 secondes
    setTimeout(() => {
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
    }, 3000);
}

// Ajout du gestionnaire d'événements au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    const addVehicleForm = document.getElementById('addVehicleForm');

    addVehicleForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(addVehicleForm);
        const data = Object.fromEntries(formData.entries());

        // Adaptation des noms de champ pour le backend
        const formattedData = {
            registrationNumber: data.registration_number,
            make: data.make,
            model: data.model,
            year: parseInt(data.year),
            rentalPrice: parseFloat(data.rental_price)
        };

        try {
            const res = await fetch(`${BASE_URL}/vehicles`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },
                body: JSON.stringify(formattedData)
            });

            if (!res.ok) {
                const errorData = await res.json();
                displayMessage('error', errorData.error || "Échec de l'ajout du véhicule.");
                return;
            }

            displayMessage('success', "Véhicule ajouté avec succès ! Redirection...");
            addVehicleForm.reset();
            setTimeout(() => {
                window.location.href = '/vehicle'; // Redirection vers la liste
            }, 1500);

        } catch (error) {
            console.error('Erreur lors de l’ajout du véhicule :', error);
            displayMessage('error', "Erreur réseau ou du serveur lors de l'ajout du véhicule.");
        }
    });
});

