"""URLs du site vitrine."""
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "vitrine"

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("a-propos/", views.apropos, name="apropos"),
    path("services/", views.services, name="services"),
    path("projets/", views.projets, name="projets"),
    path("contact/", views.contact, name="contact"),
    path("acces/", views.acces, name="acces"),
    path("demande-compte/", views.demande_compte, name="demande_compte"),
    path(
        "connexion/",
        auth_views.LoginView.as_view(template_name="vitrine/connexion.html"),
        name="connexion",
    ),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="deconnexion"),
]
