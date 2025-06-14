import { test, expect } from '@playwright/test';

test.describe('Inscription', () => {

  test('devrait permettre à un nouvel utilisateur de s\'inscrire avec succès', async ({ page }) => {
    // Mock de /users/register avec succès
    await page.route('**/users/register', async route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ message: 'Inscription réussie' })
      });
    });

    await page.goto('/register');

    const timestamp = Date.now();
    await page.fill('#username', `testuser_${timestamp}`);
    await page.fill('#email', `test${timestamp}@mail.com`);
    await page.fill('#password', 'strongpassword');

    await page.click('button[type="submit"]');

    await page.waitForURL('/');

    await expect(page).toHaveURL('/');
    await expect(page.locator('.login-container h2')).toContainText('Connexion');
  });

  test('devrait afficher un message d\'erreur si l\'utilisateur existe déjà', async ({ page }) => {
    // Mock de /users/register avec échec (utilisateur existant)
    await page.route('**/users/register', async route => {
      route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Utilisateur ou email deja existant' })
      });
    });

    await page.goto('/register');

    await page.fill('#username', 'existing_user');
    await page.fill('#email', 'existing@mail.com');
    await page.fill('#password', 'password');

    await page.click('button[type="submit"]');

    const error = page.locator('#errorMessage');
    await expect(error).toBeVisible();
    await expect(error).toContainText('Utilisateur ou email deja existant');
  });

  test('devrait naviguer vers la page de connexion', async ({ page }) => {
    await page.goto('/register');

    await page.click('.login-link a');

    await page.waitForURL('/');
    await expect(page.locator('h2')).toContainText('Connexion');
  });
});

