"""Vues de l'application suivi (accès réservé aux utilisateurs connectés)."""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import DirecteurProjet, Indicateur, Projet, Realisation, SuiviEvaluateur
from .roles import projets_accessibles, role

LIBELLES_ROLE = {
    "admin": "Administrateur",
    "coordinateur": "Coordinateur",
    "directeur": "Directeur de projet",
    "suivi": "Suivi-évaluateur",
}


def _couleur(taux):
    if taux is None:
        return "sans"
    if taux >= 90:
        return "vert"
    if taux >= 70:
        return "orange"
    return "rouge"


def _evolution(realisations):
    """Moyenne des taux de réalisation par période, dans l'ordre chronologique.

    Retourne une liste de points : libellé (ex. « T2 2026 »), taux moyen,
    hauteur de barre (plafonnée à 100) et couleur.
    """
    groupes = {}
    for realisation in realisations:
        taux = realisation.taux
        if taux is None:
            continue
        cle = (realisation.annee, realisation.periode)
        groupes.setdefault(cle, {"taux": [], "exemple": realisation})
        groupes[cle]["taux"].append(taux)
    points = []
    for cle in sorted(groupes):
        taux_liste = groupes[cle]["taux"]
        moyenne = round(sum(taux_liste) / len(taux_liste))
        points.append(
            {
                "libelle": groupes[cle]["exemple"].periode_str,
                "taux": moyenne,
                "hauteur": min(moyenne, 100),
                "couleur": _couleur(moyenne),
            }
        )
    return points


def _stats_indicateurs(indicateurs):
    """Répartition des statuts + alertes + taux global d'un lot d'indicateurs."""
    repartition = {"vert": 0, "orange": 0, "rouge": 0, "sans": 0}
    alertes, taux_valides = [], []
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
    taux_global = round(sum(taux_valides) / len(taux_valides)) if taux_valides else None
    return repartition, alertes, taux_global


@login_required
def accueil(request):
    """Tableau de bord : vue d'ensemble filtrée selon le rôle de l'utilisateur."""
    accessibles = projets_accessibles(request.user)
    indicateurs = list(
        Indicateur.objects.filter(actif=True, projet__in=accessibles).select_related("projet")
    )
    repartition, alertes, taux_global = _stats_indicateurs(indicateurs)

    total_mesures = repartition["vert"] + repartition["orange"] + repartition["rouge"]
    pourcentages = {"vert": 0, "orange": 0, "rouge": 0}
    if total_mesures:
        pourcentages = {
            cle: round(repartition[cle] / total_mesures * 100)
            for cle in ("vert", "orange", "rouge")
        }

    projets = [
        {
            "objet": projet,
            "nb_indicateurs": projet.indicateurs.filter(actif=True).count(),
            "taux": projet.taux_moyen,
        }
        for projet in accessibles.order_by("code")
    ]
    directeurs = [
        {"objet": d, "nb_projets": d.projets.count(), "taux": d.taux_moyen}
        for d in DirecteurProjet.objects.filter(actif=True, projets__in=accessibles).distinct()
    ]

    evolution = _evolution(
        Realisation.objects.filter(
            indicateur__actif=True, indicateur__projet__in=accessibles
        ).select_related("indicateur")
    )

    contexte = {
        "role_libelle": LIBELLES_ROLE.get(role(request.user)),
        "nb_projets": accessibles.count(),
        "nb_indicateurs": len(indicateurs),
        "taux_global": taux_global,
        "repartition": repartition,
        "pourcentages": pourcentages,
        "total_mesures": total_mesures,
        "alertes": alertes[:10],
        "nb_alertes": repartition["rouge"],
        "projets": projets,
        "directeurs": directeurs,
        "evolution": evolution,
    }
    return render(request, "suivi/accueil.html", contexte)


@login_required
def liste_projets(request):
    """Tous les projets avec leur performance et leur évolution."""
    lignes = []
    for projet in projets_accessibles(request.user).select_related("directeur").order_by("code"):
        indicateurs = list(projet.indicateurs.filter(actif=True))
        repartition, alertes, taux = _stats_indicateurs(indicateurs)
        lignes.append(
            {
                "objet": projet,
                "nb_indicateurs": len(indicateurs),
                "taux": taux,
                "couleur": _couleur(taux),
                "nb_alertes": repartition["rouge"],
            }
        )
    return render(request, "suivi/projets.html", {"lignes": lignes})


@login_required
def detail_projet(request, pk):
    """Fiche d'un projet : équipe, indicateurs, évolution."""
    projet = get_object_or_404(
        Projet.objects.select_related("directeur__coordinateur"), pk=pk
    )
    # Un directeur / suivi-évaluateur ne peut ouvrir que ses propres projets.
    if not projets_accessibles(request.user).filter(pk=pk).exists():
        raise Http404("Projet non accessible")
    indicateurs = list(projet.indicateurs.filter(actif=True))
    repartition, alertes, taux_global = _stats_indicateurs(indicateurs)
    lignes_indicateurs = [
        {
            "objet": ind,
            "taux": ind.taux_final,
            "couleur": _couleur(ind.taux_final),
            "cumul": ind.cumul_realise,
        }
        for ind in indicateurs
    ]
    evolution = _evolution(
        Realisation.objects.filter(indicateur__projet=projet, indicateur__actif=True)
        .select_related("indicateur")
    )
    contexte = {
        "projet": projet,
        "indicateurs": lignes_indicateurs,
        "taux_global": taux_global,
        "couleur_globale": _couleur(taux_global),
        "nb_alertes": repartition["rouge"],
        "evolution": evolution,
        "suivi_evaluateurs": projet.suivi_evaluateurs.all(),
    }
    return render(request, "suivi/projet_detail.html", contexte)


@login_required
def equipe(request):
    """Vue consolidée : directeurs de projet et suivi-évaluateurs."""
    directeurs = []
    for d in DirecteurProjet.objects.filter(actif=True).select_related("coordinateur"):
        projets_d = list(d.projets.all().order_by("code"))
        directeurs.append(
            {
                "objet": d,
                "taux": d.taux_moyen,
                "couleur": _couleur(d.taux_moyen),
                "projets": [
                    {"objet": p, "taux": p.taux_moyen, "couleur": _couleur(p.taux_moyen)}
                    for p in projets_d
                ],
            }
        )
    evaluateurs = []
    for se in SuiviEvaluateur.objects.filter(actif=True):
        projets_se = list(se.projets.all().order_by("code"))
        evaluateurs.append(
            {
                "objet": se,
                "taux": se.taux_moyen,
                "couleur": _couleur(se.taux_moyen),
                "projets": projets_se,
            }
        )
    return render(
        request,
        "suivi/equipe.html",
        {"directeurs": directeurs, "evaluateurs": evaluateurs},
    )
