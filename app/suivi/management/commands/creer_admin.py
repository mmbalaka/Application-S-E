"""Crée le compte administrateur à partir des variables d'environnement.

Idempotent : ne réécrit pas le mot de passe si le compte existe déjà
(évite d'écraser un mot de passe changé par l'utilisateur).

Variables utilisées :
    DJANGO_SUPERUSER_USERNAME (défaut : admin)
    DJANGO_ADMIN_EMAIL        (ou DJANGO_SUPERUSER_EMAIL)
    DJANGO_SUPERUSER_PASSWORD (obligatoire à la création)
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crée le compte administrateur depuis les variables d'environnement."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_ADMIN_EMAIL") or os.environ.get(
            "DJANGO_SUPERUSER_EMAIL", ""
        )
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        utilisateur = User.objects.filter(username=username).first()
        if utilisateur:
            # Compte déjà présent : on met à jour l'e-mail et les droits, pas le mot de passe.
            utilisateur.email = email or utilisateur.email
            utilisateur.is_staff = True
            utilisateur.is_superuser = True
            utilisateur.is_active = True
            utilisateur.save()
            self.stdout.write(f"Administrateur « {username} » déjà existant — inchangé (mot de passe conservé).")
            return

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_PASSWORD non défini : administrateur non créé."
                )
            )
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Administrateur « {username} » créé."))
