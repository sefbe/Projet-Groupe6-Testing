// tests/add_vehicle.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Page d\'ajout de véhicule', () => {
    test.beforeEach(async ({ page }) => {
        // Simuler une connexion
        await page.goto('http://localhost:5000/login');
        await page.evaluate(() => {
            localStorage.setItem('access_token', 'your_mock_jwt_token');
        });

        await page.goto('http://localhost:5000/add_vehicle');
        await page.waitForSelector('#addVehicleForm', { state: 'visible' });
    });

    test('devrait afficher le formulaire d\'ajout de véhicule', async ({ page }) => {
        await expect(page.locator('h1')).toHaveText('Ajouter un nouveau véhicule');
        await expect(page.locator('#registrationNumber')).toBeVisible();
        await expect(page.locator('#make')).toBeVisible();
        await expect(page.locator('#model')).toBeVisible();
        await expect(page.locator('#year')).toBeVisible();
        await expect(page.locator('#rentalPrice')).toBeVisible();
        await expect(page.locator('button[type="submit"]')).toHaveText('Ajouter le véhicule');
        await expect(page.locator('button.btn-secondary')).toHaveText('Annuler');
    });

    test('devrait ajouter un nouveau véhicule avec succès', async ({ page }) => {
        // Interception et vérification de la requête POST
        await page.route('**/vehicles', async route => {
  const raw = await route.request().postData(); // JSON string
  const postData = JSON.parse(raw!);            

  expect(postData).toEqual({
    registrationNumber: 'NEW-ADD-123',
    make: 'Tesla',
    model: 'Model 3',
    year: 2023,
    rentalPrice: 60000
  });

  await route.fulfill({
    status: 201,
    contentType: 'application/json',
    body: JSON.stringify({ message: 'Vehicle added successfully' }),
  });
});



        await page.locator('#registrationNumber').fill('NEW-ADD-123');
        await page.locator('#make').fill('Tesla');
        await page.locator('#model').fill('Model 3');
        await page.locator('#year').fill('2023');
        await page.locator('#rentalPrice').fill('60000');

        await page.locator('button[type="submit"]').click();

        //await expect(page.locator('#successMessage')).toHaveText('Véhicule ajouté avec succès ! Redirection...');
        await expect(page).toHaveURL('http://localhost:5000/add_vehicle');
    });

    test('devrait afficher une erreur pour des données de véhicule invalides', async ({ page }) => {
        await page.route('**/vehicles', async route => {
            await route.fulfill({
                status: 400,
                contentType: 'application/json',
                body: JSON.stringify({ error: 'Registration number already exists' }),
            });
        });

        await page.locator('#registrationNumber').fill('EXISTING-REG');
        await page.locator('#make').fill('Generic');
        await page.locator('#model').fill('Car');
        await page.locator('#year').fill('2020');
        await page.locator('#rentalPrice').fill('10000');

        await page.locator('button[type="submit"]').click();

        await expect(page.locator('#errorMessage')).toHaveText('Registration number already exists');
        await expect(page).toHaveURL('http://localhost:5000/add_vehicle');
    });

    test('devrait naviguer vers la liste des véhicules lorsque le bouton Annuler est cliqué', async ({ page }) => {
        await page.locator('button.btn-secondary').click();
        await expect(page).toHaveURL('http://localhost:5000/vehicle');
    });

    test('devrait rediriger si le token est manquant', async ({ page }) => {
        await page.evaluate(() => localStorage.removeItem('access_token'));
        await page.goto('http://localhost:5000/add_vehicle');
        await expect(page).toHaveURL('http://localhost:5000/');
    });
});

