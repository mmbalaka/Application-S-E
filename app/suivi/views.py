"""Vues de l'application suivi (accès réservé aux utilisateurs connectés)."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def accueil(request):
    """Page d'accueil de l'application S&E (provisoire, futur tableau de bord)."""
    return render(request, "suivi/accueil.html")
