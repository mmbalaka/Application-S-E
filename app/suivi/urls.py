"""URLs de l'application suivi."""
from django.urls import path

from . import views

app_name = "suivi"

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("projets/", views.liste_projets, name="projets"),
    path("projet/<int:pk>/", views.detail_projet, name="projet"),
    path("equipe/", views.equipe, name="equipe"),
]
