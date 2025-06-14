document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorDiv = document.getElementById("errorMessage");

    try {
        const response = await fetch('/users/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })  // role is "user" by default
        });

        const data = await response.json();

        if (!response.ok) {
            errorDiv.textContent = data.error || "Error creating account."; // Changed to English
            return;
        }

        // Use a message box or redirect directly instead of alert()
        // alert("Account created successfully!"); // Removed alert()
        window.location.href = "/"; // Redirect to login page after successful registration
    } catch (error) {
        errorDiv.textContent = "Error during request."; // Changed to English
    }
});

