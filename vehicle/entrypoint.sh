#!/bin/sh

echo "Attente du démarrage de la base de données..."
while ! nc -z db 3306; do
  sleep 1
done

echo "Base de données en ligne. Application en cours de migration..."
flask db upgrade

echo "Lancement de l'application Flask..."
exec python run.py

