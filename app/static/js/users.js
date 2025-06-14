// static/js/users.js


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
    // Hide the message after a few seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
    }, 3000);
}

document.addEventListener("DOMContentLoaded", () => {
    const BASE_URL = "http://localhost:5000";
    const token = localStorage.getItem("access_token");

    const userList = document.getElementById("user-list");
    const errorMessage = document.getElementById("errorMessage");

    // Redirection si non connecté
    if (!token) {
        console.warn("Token JWT manquant. Redirection...");
        errorMessage.innerText = "Vous devez être connecté pour voir les utilisateurs.";
        window.location.href = "/"; // Ou ta page de connexion
        return;
    }

    // Récupérer les utilisateurs
    async function fetchUsers() {
        try {
            const res = await fetch(`${BASE_URL}/users`, {
                headers: {
                    "Authorization": "Bearer " + token
                }
            });

            const responseData = await res.json();

            if (!res.ok) {
                // Token expiré ou invalide
                if (res.status === 401) {
                    localStorage.removeItem("access_token");
                    errorMessage.innerText = "Session expirée. Veuillez vous reconnecter.";
                    window.location.href = "/login.html";
                    return;
                }

                errorMessage.innerText = responseData.error || "Erreur lors du chargement des utilisateurs.";
                return;
            }

            const users = responseData.users;

            if (Array.isArray(users) && users.length > 0) {
                userList.innerHTML = "";

                users.forEach(user => {
                    const userCard = document.createElement("div");
                    userCard.className = "user-card";
                    userCard.innerHTML = `
                        <h3>${user.username}</h3>
                        <p>Email: ${user.email}</p>
                        <p>Rôle: ${user.role}</p>
                        <a href="/edit/${user.id}"><button>Modifier</button></a>
                        <button class="delete-btn" data-id="${user.id}">Supprimer</button>
                    `;
                    // Ajout du bouton de suppression
                    userCard.querySelector(".delete-btn").addEventListener("click", async (e) => {
                        const userId = e.target.dataset.id;
                        if (confirm("Supprimer cet utilisateur ?")) {
                            await deleteUser(userId);
                        }
                    });

                    userList.appendChild(userCard);
                });
            } else {
                errorMessage.innerText = "Aucun utilisateur trouvé.";
            }
        } catch (err) {
            console.error(err);
            errorMessage.innerText = "Erreur réseau.";
        }
    }

    // Supprimer un utilisateur
    async function deleteUser(userId) {
        try {
            const res = await fetch(`${BASE_URL}/users/${userId}`, {
                method: "DELETE",
                headers: {
                    "Authorization": "Bearer " + token
                }
            });

            const result = await res.json();

            if (res.ok) {
                alert("Utilisateur supprimé.");
                fetchUsers(); // Recharger la liste
            } else {
                errorMessage.innerText = result.error || "Erreur lors de la suppression.";
            }
        } catch (err) {
            console.error(err);
            errorMessage.innerText = "Erreur réseau.";
        }
    }

    // Initialisation
    fetchUsers();
});

