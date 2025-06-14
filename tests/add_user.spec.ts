import { test, expect } from '@playwright/test';

test.describe('Ajout d\'utilisateur', () => {
  const baseUrl = 'http://localhost:5000';

  test.beforeEach(async ({ page }) => {
    // Mock de la page /add_user avec formulaire et script de gestion
    await page.route('**/add_user', route => {
      route.fulfill({
        status: 200,
        contentType: 'text/html',
        body: `
          <html>
          <body>
            <h1>Ajouter un utilisateur</h1>
            <form id="add-user-form">
              <input id="username" name="username" />
              <input id="email" name="email" />
              <input id="password" name="password" />
              <input id="role" name="role" />
              <button type="submit">Créer</button>
            </form>
            <div id="errorMessage" style="display:none;color:red;"></div>

            <script>
              const form = document.getElementById('add-user-form');
              form.addEventListener('submit', async e => {
                e.preventDefault();
                const data = {
                  username: form.username.value,
                  email: form.email.value,
                  password: form.password.value,
                  role: form.role.value
                };
                try {
                  const res = await fetch('/users/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                  });
                  if(res.ok) {
                    localStorage.setItem('access_token', 'fake-token');
                    window.location.href = '/user';
                  } else {
                    const err = await res.text();
                    const errorEl = document.getElementById('errorMessage');
                    errorEl.style.display = 'block';
                    errorEl.innerText = err || 'Erreur lors de la création';
                  }
                } catch (err) {
                  const errorEl = document.getElementById('errorMessage');
                  errorEl.style.display = 'block';
                  errorEl.innerText = 'Erreur réseau';
                }
              });
            </script>
          </body>
          </html>
        `
      });
    });

    // Mock de la route POST /users/register pour simuler la création utilisateur
    await page.route('**/users/register', route => {
      const postData = JSON.parse(route.request().postData() || '{}');
      // Simple validation mock
      if (postData.email && postData.email.includes('@')) {
        route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ success: true, userId: 123 })
        });
      } else {
        route.fulfill({
          status: 400,
          contentType: 'text/plain',
          body: 'Email invalide'
        });
      }
    });
  });

  test('Créer un nouvel utilisateur avec succès', async ({ page }) => {
    await page.goto(`${baseUrl}/add_user`);

    const usernameInput = page.locator('#username');
    await expect(usernameInput).toBeVisible();

    await usernameInput.fill('testuser');
    await page.fill('#email', 'testuser@example.com');
    await page.fill('#password', 'Test1234!');
    await page.fill('#role', 'user');

    // Intercepter la requête POST
    const [response] = await Promise.all([
      page.waitForResponse(resp => resp.url().endsWith('/users/register') && resp.status() === 200),
      page.click('button[type="submit"]'),
    ]);

    expect(response.ok()).toBe(true);

    // Attendre la redirection
    await page.waitForURL(/\/user/);

    // Vérifier que le token a été stocké en localStorage
    const token = await page.evaluate(() => localStorage.getItem('access_token'));
    expect(token).toBe('fake-token');
  });

  test('Affiche une erreur si email invalide', async ({ page }) => {
    await page.goto(`${baseUrl}/add_user`);

    await page.fill('#username', 'invalidmailuser');
    await page.fill('#email', 'notanemail');
    await page.fill('#password', 'Test1234!');
    await page.fill('#role', 'user');

    await page.click('button[type="submit"]');

    const errorMessage = page.locator('#errorMessage');
    // Attendre que le message d'erreur soit visible
    await errorMessage.waitFor({ state: 'visible' });

    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText(/email invalide/i);
  });
});

