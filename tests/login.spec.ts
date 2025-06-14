// tests/login.spec.ts
// Ce fichier contient le test de connexion à l'application.

import { test, expect } from '@playwright/test';

test.describe('Interface de connexion (/login)', () => {

  // Test: Vérifier qu’un utilisateur peut se connecter avec des identifiants valides.
  test('devrait permettre à un utilisateur de se connecter avec des identifiants valides', async ({ page }) => {
    // Naviguer vers la page de connexion.
    await page.goto('/'); // Le fichier login.html est la page d'accueil (racine /)

    // Vérifier la présence des champs de formulaire spécifiques
    await expect(page.locator('#username')).toBeVisible();
    await expect(page.locator('#password')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();

    // Remplir le champ de nom d'utilisateur par son ID
    // REMPLACEZ 'utilisateur_test' par un nom d'utilisateur valide pour votre application.
    await page.locator('#username').fill('ronel');

    // Remplir le champ de mot de passe par son ID
    // REMPLACEZ 'motdepasse123' par un mot de passe valide pour votre application.
    await page.locator('#password').fill('ronel');

    // Cliquer sur le bouton de connexion par son type
    await page.locator('button[type="submit"]').click();

    // Attendre que la navigation soit terminée vers la page /vehicle (comme indiqué dans login.html)
    await page.waitForURL('/vehicle');

    // Vérifier que l'URL est bien celle du tableau de bord des véhicules.
    await expect(page).toHaveURL('/vehicle');

    // Vérifier un élément sur la page des véhicules pour confirmer la connexion
    await expect(page.locator('h1')).toContainText('Tableau de bord – Véhicules');
  });

  // Test: Vérifier qu'un message d'erreur est affiché avec des identifiants invalides.
  test('devrait afficher un message d\'erreur avec des identifiants invalides', async ({ page }) => {
    await page.goto('/');

    // Remplir avec des identifiants invalides
    await page.locator('#username').fill('mauvais_utilisateur');
    await page.locator('#password').fill('mauvais_motdepasse');
    await page.locator('button[type="submit"]').click();

    // Attendre que le message d'erreur par son ID devienne visible et contienne le texte attendu
    const errorMessage = page.locator('#errorMessage');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText('Identifiants invalides'); // Texte tel que configuré dans login.html
  });

  // Test: Vérifier la navigation vers la page d'inscription.
  test('devrait naviguer vers la page d\'inscription', async ({ page }) => {
    await page.goto('/');

    // Cliquer sur le lien "Créer un compte"
    await page.locator('.register-link a').click();

    // Attendre la redirection vers la page /register
    await page.waitForURL('/register');

    // Vérifier que le titre de la page d'inscription est présent
    await expect(page.locator('h2')).toContainText('Créer un compte');
  });
});
