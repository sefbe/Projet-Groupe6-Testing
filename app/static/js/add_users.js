// static/js/add_users.js
document.addEventListener("DOMContentLoaded", function () {
    const userForm = document.getElementById("userForm");
    const BASE_URL = "http://localhost:5000";

    if (!userForm) {
        console.error("Formulaire introuvable !");
        return;
    }

    userForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(userForm);
        const data = {
            username: formData.get("username"),
            email: formData.get("email"),
            password: formData.get("password"),
            role: formData.get("role")
        };

        try {
            // Étape 1 : enregistrement
            const registerRes = await fetch(`${BASE_URL}/users/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const registerResult = await registerRes.json();

            if (!registerRes.ok) {
                document.getElementById("errorMessage").innerText = registerResult.error || "Erreur lors de l'enregistrement.";
                return;
            }

            // Étape 2 : login automatique
            const loginRes = await fetch(`${BASE_URL}/users/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: data.username,
                    password: data.password
                })
            });

            const loginResult = await loginRes.json();

            if (loginRes.ok) {
                // Stocker le token JWT
                localStorage.setItem("access_token", loginResult.access_token);
                alert("Utilisateur enregistré et connecté !");
                window.location.href = "/user";
            } else {
                document.getElementById("errorMessage").innerText = loginResult.error || "Utilisateur créé mais connexion échouée.";
            }
        } catch (err) {
            console.error(err);
            document.getElementById("errorMessage").innerText = "Erreur réseau ou JSON.";
        }
    });
});

