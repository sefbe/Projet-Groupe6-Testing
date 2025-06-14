import { test, expect } from '@playwright/test';

test.describe('Formulaire modification utilisateur (mocké)', () => {
  const USER_ID = 275;
  const MOCK_URL = `http://localhost:5000/edit_user/${USER_ID}`;
  const API_URL = `http://localhost:5000/users/${USER_ID}`;

  const MOCK_HTML = `
  <!DOCTYPE html>
  <html lang="fr">
  <head>
    <meta charset="UTF-8">
    <title>Modifier un utilisateur</title>
  </head>
  <body>
    <form id="userEditForm">
      <input type="hidden" name="id" value="${USER_ID}">
      <input type="text" name="username" value="ancien_nom" placeholder="Nom d'utilisateur" required><br>
      <input type="email" name="email" value="ancien@mail.com" placeholder="Adresse e-mail" required><br>
      <input type="password" name="password" placeholder="Nouveau mot de passe"><br>
      <input type="text" name="role" value="user" placeholder="Rôle" required><br>
      <button type="submit">Enregistrer</button>
    </form>

    <script>
      const userId = ${USER_ID};
      const token = localStorage.getItem('access_token');
      const BASE_URL = 'http://localhost:5000';

      document.getElementById('userEditForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const data = {
          username: form.username.value,
          email: form.email.value,
          role: form.role.value,
          ...(form.password.value && { password: form.password.value })
        };

        const res = await fetch(\`\${BASE_URL}/users/\${userId}\`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify(data)
        });

        if (!res.ok) {
          const errorData = await res.json();
          alert(errorData.error || "Erreur lors de la modification.");
          return;
        }

        window.location.href = "/user";
      });
    </script>
  </body>
  </html>
  `;

  test('modifie un utilisateur avec données mockées', async ({ page }) => {
    // Mock la page HTML
    await page.route(MOCK_URL, async route => {
      await route.fulfill({
        contentType: 'text/html',
        body: MOCK_HTML
      });
    });

    // Mock PUT /users/ID
    await page.route(API_URL, async route => {
      const req = route.request();
      const data = JSON.parse(req.postData() || '{}');

      // Assertions sur les données envoyées
      expect(data.username).toBe('modif_nom');
      expect(data.email).toBe('modif@mail.com');
      expect(data.role).toBe('admin');
      expect(data.password).toBe('Nouveau123');

      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ message: 'Mise à jour réussie' })
      });
    });

    // Simule un token local
    await page.addInitScript(() => {
      localStorage.setItem('access_token', 'fake_token');
    });

    // Aller à la page (mockée)
    await page.goto(MOCK_URL);

    // Remplir le formulaire
    await page.fill('input[name="username"]', 'modif_nom');
    await page.fill('input[name="email"]', 'modif@mail.com');
    await page.fill('input[name="password"]', 'Nouveau123');
    await page.fill('input[name="role"]', 'admin');

    // Soumettre
    await Promise.all([
      page.waitForURL('/user'),
      page.click('button[type="submit"]')
    ]);
  });
});

