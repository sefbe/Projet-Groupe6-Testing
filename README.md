# 🚀 Projet-Groupe6-Testing

Projet de tests automatisés combinant :
- ✅ **Backend en Python** avec **Flask** et **Pytest**
- ✅ **Frontend testé avec Playwright** en **TypeScript**



## Structure du projet

Projet-Groupe6-Testing/
│
├── app/ # Application Flask + tests backend
│ └── tests/ # Tests unitaires et d'intégration (Pytest)
│
├── tests/ # Tests end-to-end (E2E) avec Playwright
│
├── run.py # Point d'entrée de l'application
├── requirements.txt # Dépendances Python
├── Dockerfile # Docker (optionnel)
├── Makefile # Commandes automatisées
└── README.md # Ce fichier

##  Installation

###  1. Installer les dépendances Python

python -m venv venv
source venv/bin/activate       # Sous Windows : venv\Scripts\activate
pip install -r requirements.txt

### 2. Installer Playwright
Si package.json n'existe pas encore :

npm init -y
npm install -D playwright
npx playwright install

### Exécution des tests
##🔹 Tests backend (Python + Pytest)

make test-backend

##🔹 Tests frontend (Playwright + TypeScript)

make test-frontend

## Tout installer d'un coup (backend + frontend)

make install

### Commandes Makefile disponibles

make install        # Installe les dépendances backend et frontend
make test-backend   # Exécute tous les tests Python (Pytest)
make test-frontend  # Exécute tous les tests Playwright

### Technologies utilisées
Python 3.8

Flask

Pytest

Playwright

TypeScript

Docker

### Auteurs
Groupe 6 – Projet de testing logiciel.

-MAAMOC KENGUIM RONEL
-SEFADINE ALI IDRISS
-MBANDA PAMBI NAOMI PASCALE
-EBAI BATE LUCKY BETTY
-NKONE MAPOURE AICHA SELIMA
-KAMDEM WANDJI IDRISS
