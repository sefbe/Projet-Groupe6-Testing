document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorDiv = document.getElementById("errorMessage");

    try {
        const response = await fetch('/users/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (!response.ok) {
            errorDiv.textContent = data.error || "Identifiants invalides.";
            return;
        }

        localStorage.setItem("access_token", data.access_token);
        window.location.href = "/vehicle";  // Redirection après connexion
    } catch (error) {
        errorDiv.textContent = "Erreur lors de la connexion.";
    }
});

