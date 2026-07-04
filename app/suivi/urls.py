"""URLs de l'application suivi."""
from django.urls import path

from . import views

app_name = "suivi"

urlpatterns = [
    path("", views.accueil, name="accueil"),
]
