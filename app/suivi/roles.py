"""Modèle de rôles et de permissions du suivi-évaluation.

Rôles (groupes Django) et cardinalités :

    Administrateur (superuser) — rôle technique, accès complet.
    Coordinateur               — un seul, supervise TOUS les projets (niveau global, lecture).
    Directeur                  — 1 directeur → N projets ; gère le cadre de mesure de SES projets.
    Suivi-évaluateur           — 1 SE → N projets ; saisit les réalisations de SES projets.

La restriction « ses projets » (niveau ligne) est appliquée dans l'admin
(get_queryset + has_*_permission), au-dessus des permissions de modèle des groupes.
"""

GROUPE_COORDINATEUR = "Coordinateur"
GROUPE_DIRECTEUR = "Directeur"
GROUPE_SUIVI = "Suivi-évaluateur"

TOUS_LES_GROUPES = (GROUPE_COORDINATEUR, GROUPE_DIRECTEUR, GROUPE_SUIVI)


def role(user):
    """Retourne le rôle de l'utilisateur : admin / coordinateur / directeur / suivi / None."""
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return "admin"
    noms = set(user.groups.values_list("name", flat=True))
    if GROUPE_COORDINATEUR in noms:
        return "coordinateur"
    if GROUPE_DIRECTEUR in noms:
        return "directeur"
    if GROUPE_SUIVI in noms:
        return "suivi"
    return None


def projets_accessibles(user):
    """QuerySet des projets que l'utilisateur peut voir selon son rôle."""
    from .models import Projet

    r = role(user)
    if r in ("admin", "coordinateur"):
        return Projet.objects.all()
    if r == "directeur":
        return Projet.objects.filter(directeur__utilisateur=user)
    if r == "suivi":
        return Projet.objects.filter(suivi_evaluateurs__utilisateur=user).distinct()
    return Projet.objects.none()


def peut_modifier_projet(user, projet):
    """Un projet donné est-il modifiable par cet utilisateur ?"""
    r = role(user)
    if r in ("admin", "coordinateur"):
        return True
    if r == "directeur" and projet is not None:
        return bool(projet.directeur_id) and projet.directeur.utilisateur_id == user.id
    return False
