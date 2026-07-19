#!/usr/bin/env bash
# Script de construction exécuté par l'hébergeur (Render) à chaque déploiement.
set -o errexit

pip install -r requirements.txt
python scripts/compile_translations.py          # traductions FR/EN
python manage.py collectstatic --noinput         # fichiers de style
python manage.py migrate                          # base de données à jour
python manage.py configurer_roles                 # groupes de rôles + permissions
python manage.py creer_admin                      # compte administrateur (si défini)
