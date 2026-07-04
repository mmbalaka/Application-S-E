"""Vues de l'application suivi."""
from django.shortcuts import render


def accueil(request):
    """Page d'accueil provisoire (démonstration du bilinguisme)."""
    return render(request, "suivi/accueil.html")
