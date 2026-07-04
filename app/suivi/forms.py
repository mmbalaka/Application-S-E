"""Formulaires de l'application suivi."""
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Projet


class ImportIndicateursForm(forms.Form):
    """Téléversement d'une liste d'indicateurs (CSV ou Excel) pour un projet."""

    projet = forms.ModelChoiceField(
        queryset=Projet.objects.all(),
        label=_("Projet"),
        help_text=_("Les indicateurs importés seront rattachés à ce projet."),
    )
    fichier = forms.FileField(
        label=_("Fichier CSV ou Excel"),
        help_text=_("Formats acceptés : .csv, .xlsx — la première ligne doit contenir les entêtes."),
    )
