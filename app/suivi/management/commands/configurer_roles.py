"""Crée (ou met à jour) les groupes de rôles et leurs permissions.

Idempotent : peut être relancé sans risque.
    python manage.py configurer_roles
"""
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from suivi.roles import GROUPE_COORDINATEUR, GROUPE_DIRECTEUR, GROUPE_SUIVI

# Permissions par groupe : (modèle, [verbes])
# verbes possibles : view, add, change, delete
MATRICE = {
    GROUPE_COORDINATEUR: {
        # Supervision globale : lit tout ; pilote les projets (crée, modifie, affecte)
        "projet": ["view", "add", "change", "delete"],
        "indicateur": ["view"],
        "cible": ["view"],
        "realisation": ["view"],
        "sourceverification": ["view"],
        "ventilationrealisation": ["view"],
        "axedesagregation": ["view"],
        "coordinateur": ["view"],
        "directeurprojet": ["view", "add", "change"],
        "suivievaluateur": ["view", "add", "change"],
    },
    GROUPE_DIRECTEUR: {
        # Cadre de mesure de SES projets : indicateurs + cibles
        "projet": ["view", "change"],
        "indicateur": ["view", "add", "change", "delete"],
        "cible": ["view", "add", "change", "delete"],
        "realisation": ["view"],
        "sourceverification": ["view"],
        "ventilationrealisation": ["view"],
        "axedesagregation": ["view"],
    },
    GROUPE_SUIVI: {
        # Collecte de SES projets : réalisations + sources + ventilations
        "projet": ["view"],
        "indicateur": ["view"],
        "cible": ["view"],
        "realisation": ["view", "add", "change", "delete"],
        "sourceverification": ["view", "add", "change", "delete"],
        "ventilationrealisation": ["view", "add", "change", "delete"],
        "axedesagregation": ["view"],
    },
}


class Command(BaseCommand):
    help = "Crée les groupes de rôles (Coordinateur, Directeur, Suivi-évaluateur) et leurs permissions."

    def handle(self, *args, **options):
        for nom_groupe, modeles in MATRICE.items():
            groupe, _ = Group.objects.get_or_create(name=nom_groupe)
            permissions = []
            for modele, verbes in modeles.items():
                for verbe in verbes:
                    codename = f"{verbe}_{modele}"
                    try:
                        permissions.append(
                            Permission.objects.get(
                                codename=codename,
                                content_type__app_label="suivi",
                            )
                        )
                    except Permission.DoesNotExist:
                        self.stderr.write(f"  ! permission introuvable : suivi.{codename}")
            groupe.permissions.set(permissions)
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Groupe « {nom_groupe} » : {len(permissions)} permission(s) configurée(s)."
                )
            )
        self.stdout.write(self.style.SUCCESS("Rôles configurés."))
