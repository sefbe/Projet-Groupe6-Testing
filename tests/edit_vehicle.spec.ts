// tests/edit_vehicle.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Page de modification de véhicule', () => {
    const vehicleId = 123; // ID fictif pour les tests

    test.beforeEach(async ({ page }) => {
        // Simuler une connexion en insérant un token dans le localStorage
        await page.goto('http://localhost:5000/login');
        await page.evaluate(() => {
            localStorage.setItem('access_token', 'your_mock_jwt_token');
        });

        // Interception de la requête GET pour charger les données du véhicule
        await page.route(`**/vehicles/${vehicleId}`, async route => {
            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({
                    vehicle: {
                        id: vehicleId,
                        registrationNumber: 'OLD-REG-123',
                        make: 'Audi',
                        model: 'A4',
                        year: 2015,
                        rentalPrice: 30000
                    }
                }),
            });
        });

        await page.goto(`http://localhost:5000/vehicles/${vehicleId}/edit`);
        await page.waitForSelector('#editVehicleForm', { state: 'visible' });
    });

    test('devrait charger les données du véhicule existant dans le formulaire', async ({ page }) => {
        await expect(page.locator('h1')).toHaveText('Modifier un véhicule');
        await expect(page.locator('#vehicleId')).toHaveValue(String(vehicleId));
        await expect(page.locator('#registrationNumber')).toHaveValue('OLD-REG-123');
        await expect(page.locator('#make')).toHaveValue('Audi');
        await expect(page.locator('#model')).toHaveValue('A4');
        await expect(page.locator('#year')).toHaveValue('2015');
        await expect(page.locator('#rentalPrice')).toHaveValue('30000');
    });

    test('devrait mettre à jour les données du véhicule avec succès', async ({ page }) => {
        // Interception de la requête PUT pour mise à jour
        await page.route(`**/vehicles/5`, async route => {
            const requestBody = await route.request().postDataJSON();
            console.log('Payload reçu :', requestBody); // Pour debug

            expect(requestBody.registrationNumber).toBe('UPDATED-REG-456');
            expect(requestBody.make).toBe('BMW');
            expect(requestBody.model).toBe('X3');
            expect(requestBody.year).toBe(2020);
            expect(requestBody.rentalPrice).toBe(45000);

            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({ message: 'Vehicle updated successfully' }),
            });
        });

        // Remplir le formulaire avec les nouvelles données
        await page.locator('#registrationNumber').fill('UPDATED-REG-456');
        await page.locator('#make').fill('BMW');
        await page.locator('#model').fill('X3');
        await page.locator('#year').fill('2020');
        await page.locator('#rentalPrice').fill('45000');

        // Soumettre le formulaire
        await page.locator('button[type="submit"]').click();

        // Attendre le message de succès et la redirection
        //await expect(page.locator('#successMessage')).toHaveText('Véhicule modifié avec succès ! Redirection...');
        await expect(page).toHaveURL('http://localhost:5000/vehicle');
    });

    test('devrait afficher une erreur pour des données de mise à jour invalides', async ({ page }) => {
        await page.route(`**/vehicles/${vehicleId}`, async route => {
            await route.fulfill({
                status: 400,
                contentType: 'application/json',
                body: JSON.stringify({ error: 'Invalid data provided for update' }),
            });
        });

        await page.locator('#year').fill('1800'); // Valeur invalide

        await page.locator('button[type="submit"]').click();

        //await expect(page.locator('#errorMessage')).toHaveText('Invalid data provided for update');
        await expect(page).toHaveURL(`http://localhost:5000/vehicles/${vehicleId}/edit`);
    });

    test('devrait naviguer vers la liste des véhicules lorsque le bouton Annuler est cliqué', async ({ page }) => {
        await page.locator('button.btn-secondary').click();
        await expect(page).toHaveURL('http://localhost:5000/vehicle');
    });

    test('devrait rediriger si le token est manquant', async ({ page }) => {
        await page.evaluate(() => localStorage.removeItem('access_token'));
        await page.goto(`http://localhost:5000/vehicles/${vehicleId}/edit`);
        await expect(page).toHaveURL('http://localhost:5000/');
    });
});

