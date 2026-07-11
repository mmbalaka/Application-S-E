"""Vues de l'application suivi (accès réservé aux utilisateurs connectés)."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import DirecteurProjet, Indicateur, Projet


@login_required
def accueil(request):
    """Tableau de bord : vue d'ensemble de la performance des projets."""
    indicateurs = list(
        Indicateur.objects.filter(actif=True).select_related("projet")
    )

    # Statuts (selon les seuils propres à chaque indicateur)
    repartition = {"vert": 0, "orange": 0, "rouge": 0, "sans": 0}
    alertes = []
    taux_valides = []
    for ind in indicateurs:
        taux = ind.taux_final
        statut = ind.statut_pour(taux)
        if statut is None:
            repartition["sans"] += 1
        else:
            repartition[statut] += 1
            taux_valides.append(taux)
            if statut == "rouge":
                alertes.append(ind)
    alertes.sort(key=lambda i: i.taux_final)

    total_mesures = repartition["vert"] + repartition["orange"] + repartition["rouge"]
    pourcentages = {"vert": 0, "orange": 0, "rouge": 0}
    if total_mesures:
        pourcentages = {
            cle: round(repartition[cle] / total_mesures * 100)
            for cle in ("vert", "orange", "rouge")
        }

    # Performance par projet
    projets = []
    for projet in Projet.objects.all().order_by("code"):
        projets.append(
            {
                "objet": projet,
                "nb_indicateurs": projet.indicateurs.filter(actif=True).count(),
                "taux": projet.taux_moyen,
            }
        )

    # Performance par directeur (portefeuilles)
    directeurs = []
    for directeur in DirecteurProjet.objects.filter(actif=True):
        directeurs.append(
            {
                "objet": directeur,
                "nb_projets": directeur.projets.count(),
                "taux": directeur.taux_moyen,
            }
        )

    contexte = {
        "nb_projets": Projet.objects.count(),
        "nb_indicateurs": len(indicateurs),
        "taux_global": round(sum(taux_valides) / len(taux_valides)) if taux_valides else None,
        "repartition": repartition,
        "pourcentages": pourcentages,
        "total_mesures": total_mesures,
        "alertes": alertes[:10],
        "nb_alertes": repartition["rouge"],
        "projets": projets,
        "directeurs": directeurs,
    }
    return render(request, "suivi/accueil.html", contexte)
