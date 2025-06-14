import { test, expect } from '@playwright/test';

const mockVehicles = [
  {
    id: '1',
    make: 'Toyota',
    model: 'Corolla',
    year: 2022,
    registrationNumber: 'ABC-123',
    rentalPrice: 45000
  },
  {
    id: '2',
    make: 'Honda',
    model: 'Civic',
    year: 2021,
    registrationNumber: 'XYZ-789',
    rentalPrice: 50000
  }
];

test.describe('Gestion des véhicules', () => {

  test.beforeEach(async ({ page }) => {
  await page.route('**/vehicles', route => {
    route.fulfill({
      status: 200,
      body: JSON.stringify({ vehicles: mockVehicles }),
      headers: { 'Content-Type': 'application/json' }
    });
  });

  // Injecte le token **avant** la navigation
  await page.addInitScript(() => {
    localStorage.setItem('access_token', 'mock-token');
  });

  await page.goto('http://localhost:5000/vehicle');
});

  test('Affiche tous les véhicules correctement', async ({ page }) => {
  await expect(page.locator('.vehicle-card')).toHaveCount(2);
  await expect(page.locator('.vehicle-card').first()).toContainText('Toyota Corolla');
});

  test('Filtre par immatriculation retourne un seul véhicule', async ({ page }) => {
    await page.route('**/vehicles/search/registration/ABC-123', route => {
      route.fulfill({
        status: 200,
        body: JSON.stringify(mockVehicles[0]),
        headers: { 'Content-Type': 'application/json' }
      });
    });

    await page.fill('#filter-registration', 'ABC-123');
    await page.click('text=Rechercher');

    await expect(page.locator('.vehicle-card')).toHaveCount(1);
    await expect(page.locator('.vehicle-card')).toContainText('ABC-123');
  });


  test('Clique sur "Ajouter un véhicule" redirige vers le formulaire', async ({ page }) => {
    await page.click('#add-vehicle-btn');
    await expect(page).toHaveURL('/add_vehicle');
  });

  test('Redirection vers gestion utilisateurs fonctionne', async ({ page }) => {
    await page.click('#go-to-users');
    await expect(page).toHaveURL('/user');
  });

});

