# Makefile pour automatiser les tests backend (pytest) et frontend (Playwright)

.PHONY: install test-backend test-frontend clean

# Création de l'environnement virtuel + installation des dépendances Python et Node
install:
	@echo "  Installation des dépendances Python et Node..."
	python -m venv venv && \
	source venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt && \
	cd tests && \
	if [ ! -f package.json ]; then npm init -y; fi && \
	npm install -D playwright && \
	npx playwright install

#lancer l'application
run:
	@echo "Demarrage du serveur"
	python3 run.py

# Exécution des tests Python (backend)
test-backend:
	@echo " Lancement des tests Pytest (backend)..."
	source venv/bin/activate && \
	pytest app/tests/

# Exécution des tests Playwright (frontend)
test-frontend:
	@echo " Lancement des tests Playwright (frontend)..."
	python3 run.py && \
	cd tests && \
	npx playwright test

# Nettoyage des fichiers temporaires
clean:
	@echo "🧹 Nettoyage..."
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	rm -rf .pytest_cache htmlcov venv

