"""Modèles de données — structure organisationnelle du suivi-évaluation.

Hiérarchie : Coordinateur (1-N) Directeur de projet (1-N) Projet (N-N) Suivi-évaluateur.
Le nombre de projets et d'intervenants est entièrement libre (aucune limite).
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class PersonneBase(models.Model):
    """Champs communs à tous les intervenants."""

    nom = models.CharField(_("nom complet"), max_length=150)
    email = models.EmailField(_("adresse e-mail"), blank=True)
    telephone = models.CharField(_("téléphone"), max_length=30, blank=True)
    actif = models.BooleanField(_("actif"), default=True)

    class Meta:
        abstract = True
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Coordinateur(PersonneBase):
    """Coordinateur : supervise un ou plusieurs directeurs de projet."""

    class Meta(PersonneBase.Meta):
        verbose_name = _("coordinateur")
        verbose_name_plural = _("coordinateurs")


class DirecteurProjet(PersonneBase):
    """Directeur de projet : rattaché à un coordinateur, dirige plusieurs projets."""

    coordinateur = models.ForeignKey(
        Coordinateur,
        verbose_name=_("coordinateur"),
        related_name="directeurs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Coordinateur dont dépend ce directeur de projet."),
    )

    class Meta(PersonneBase.Meta):
        verbose_name = _("directeur de projet")
        verbose_name_plural = _("directeurs de projet")


class SuiviEvaluateur(PersonneBase):
    """Suivi-évaluateur : peut intervenir sur plusieurs projets."""

    class Meta(PersonneBase.Meta):
        verbose_name = _("suivi-évaluateur")
        verbose_name_plural = _("suivi-évaluateurs")


class Projet(models.Model):
    """Projet mis en œuvre par l'association."""

    class Statut(models.TextChoices):
        EN_PREPARATION = "preparation", _("En préparation")
        EN_COURS = "en_cours", _("En cours")
        CLOTURE = "cloture", _("Clôturé")

    code = models.CharField(
        _("code"),
        max_length=20,
        unique=True,
        help_text=_("Code court et unique du projet (ex. : AGR-01)."),
    )
    nom = models.CharField(_("nom du projet"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    domaine = models.CharField(
        _("domaine d'intervention"),
        max_length=100,
        blank=True,
        help_text=_("Ex. : agriculture, éducation, santé…"),
    )
    date_debut = models.DateField(_("date de début"), null=True, blank=True)
    date_fin = models.DateField(_("date de fin"), null=True, blank=True)
    statut = models.CharField(
        _("statut"), max_length=20, choices=Statut.choices, default=Statut.EN_COURS
    )
    directeur = models.ForeignKey(
        DirecteurProjet,
        verbose_name=_("directeur de projet"),
        related_name="projets",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=_("Directeur responsable de ce projet."),
    )
    suivi_evaluateurs = models.ManyToManyField(
        SuiviEvaluateur,
        verbose_name=_("suivi-évaluateurs"),
        related_name="projets",
        blank=True,
        help_text=_("Un projet peut être suivi par plusieurs suivi-évaluateurs."),
    )

    class Meta:
        verbose_name = _("projet")
        verbose_name_plural = _("projets")
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} — {self.nom}"
