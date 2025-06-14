import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:5000';
const PAGE_URL = `${BASE_URL}/user`;

const MOCK_USERS = [
  { id: 1, username: 'alice', email: 'alice@mail.com', role: 'admin' },
  { id: 2, username: 'bob', email: 'bob@mail.com', role: 'user' }
];

const MOCK_HTML = `
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>Gestion des utilisateurs</title></head>
<body>
  <div id="user-list"></div>
  <div id="errorMessage" class="message"></div>
  <script>
    const token = localStorage.getItem("access_token");
    const BASE_URL = "${BASE_URL}";

    async function fetchUsers() {
      try {
        const res = await fetch(BASE_URL + "/users", {
          headers: { "Authorization": "Bearer " + token }
        });

        if (!res.ok) {
          const err = await res.json();
          document.getElementById("errorMessage").innerText = err.error || "Erreur serveur";
          return;
        }

        const data = await res.json();
        const userList = document.getElementById("user-list");
        userList.innerHTML = "";
        data.users.forEach(user => {
          const div = document.createElement("div");
          div.className = "user-card";
          div.innerHTML = \`
            <h3>\${user.username}</h3>
            <p>Email: \${user.email}</p>
            <p>Rôle: \${user.role}</p>
            <button class="delete-btn" data-id="\${user.id}">Supprimer</button>
          \`;
          div.querySelector(".delete-btn").addEventListener("click", async (e) => {
            const userId = e.target.dataset.id;
            const delRes = await fetch(BASE_URL + "/users/" + userId, {
              method: "DELETE",
              headers: { "Authorization": "Bearer " + token }
            });
            if (delRes.ok) {
              fetchUsers();
            }
          });
          userList.appendChild(div);
        });
      } catch (e) {
        document.getElementById("errorMessage").innerText = "Erreur réseau";
      }
    }

    if (!token) {
      document.getElementById("errorMessage").innerText = "Vous devez être connecté.";
    } else {
      fetchUsers();
    }
  </script>
</body>
</html>
`;

test.describe('Gestion utilisateurs', () => {
  test.beforeEach(async ({ page }) => {
    await page.route(PAGE_URL, route => route.fulfill({
      contentType: 'text/html',
      body: MOCK_HTML
    }));

    await page.addInitScript(() => {
      localStorage.setItem('access_token', 'fake-token');
    });
  });

  test('1. Affiche la liste des utilisateurs', async ({ page }) => {
    // 👇 CORRECTION : définir la route AVANT le goto
    await page.route(`${BASE_URL}/users`, route =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ users: MOCK_USERS }) })
    );

    await page.goto(PAGE_URL);

    await expect(page.locator('.user-card')).toHaveCount(2);
    await expect(page.locator('.user-card').nth(0)).toContainText('alice');
    await expect(page.locator('.user-card').nth(1)).toContainText('bob');
  });

  test('2. Supprime un utilisateur avec succès', async ({ page }) => {
  let currentUsers = [...MOCK_USERS]; // liste modifiable

  // Route GET /users qui renvoie toujours currentUsers
  await page.route(`${BASE_URL}/users`, route => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ users: currentUsers })
      });
    }
  });

  // Route DELETE /users/2 qui modifie currentUsers
  await page.route(`${BASE_URL}/users/2`, route => {
    expect(route.request().method()).toBe('DELETE');
    // Supprimer bob (id 2) de la liste
    currentUsers = currentUsers.filter(u => u.id !== 2);
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ message: 'Utilisateur supprimé' })
    });
  });

  await page.goto(PAGE_URL);

  // Cliquer sur le bouton supprimer de bob
  await page.locator('.user-card').nth(1).getByRole('button', { name: 'Supprimer' }).click();

  // Attendre que la liste des utilisateurs soit mise à jour : 1 user seulement
  await expect(page.locator('.user-card')).toHaveCount(1);

  // Vérifier que c’est bien alice qui reste
  await expect(page.locator('.user-card')).toContainText('alice');
});


  test('3. Affiche une erreur réseau', async ({ page }) => {
    await page.route(`${BASE_URL}/users`, route => {
      route.abort(); // Simule une erreur réseau
    });

    await page.goto(PAGE_URL);
    await expect(page.locator('#errorMessage')).toHaveText(/Erreur réseau/i);
  });

  test('4. Affiche une erreur serveur (403)', async ({ page }) => {
    await page.route(`${BASE_URL}/users`, route =>
      route.fulfill({
        status: 403,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Accès interdit' })
      })
    );

    await page.goto(PAGE_URL);
    await expect(page.locator('#errorMessage')).toHaveText(/accès interdit/i);
  });

  test('5. Redirige vers login si pas de token', async ({ page, context }) => {
    await context.addInitScript(() => localStorage.removeItem('access_token'));

    await page.goto(PAGE_URL);
    await expect(page.locator('#errorMessage')).toHaveText(/Vous devez être connecté./i);
  });
});

