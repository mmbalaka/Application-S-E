"""Modèles du site vitrine : demandes de compte et messages de contact."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class DemandeCompte(models.Model):
    """Demande d'accès à l'application, soumise à l'approbation de l'administrateur."""

    class Statut(models.TextChoices):
        EN_ATTENTE = "en_attente", _("En attente")
        APPROUVEE = "approuvee", _("Approuvée")
        REFUSEE = "refusee", _("Refusée")

    nom = models.CharField(_("nom complet"), max_length=150)
    email = models.EmailField(_("adresse e-mail"), unique=True)
    organisation = models.CharField(_("organisation"), max_length=150, blank=True)
    fonction = models.CharField(_("fonction"), max_length=150, blank=True)
    motif = models.TextField(
        _("motif de la demande"),
        help_text=_("Pourquoi souhaitez-vous accéder à l'application ?"),
    )
    statut = models.CharField(
        _("statut"), max_length=15, choices=Statut.choices, default=Statut.EN_ATTENTE
    )
    date_demande = models.DateTimeField(_("date de la demande"), auto_now_add=True)
    date_traitement = models.DateTimeField(_("date de traitement"), null=True, blank=True)

    class Meta:
        verbose_name = _("demande de compte")
        verbose_name_plural = _("demandes de compte")
        ordering = ["-date_demande"]

    def __str__(self):
        return f"{self.nom} <{self.email}>"


class MessageContact(models.Model):
    """Message envoyé depuis le formulaire de contact du site."""

    nom = models.CharField(_("nom"), max_length=150)
    email = models.EmailField(_("adresse e-mail"))
    sujet = models.CharField(_("sujet"), max_length=200)
    message = models.TextField(_("message"))
    date_envoi = models.DateTimeField(_("date d'envoi"), auto_now_add=True)
    traite = models.BooleanField(_("traité"), default=False)

    class Meta:
        verbose_name = _("message de contact")
        verbose_name_plural = _("messages de contact")
        ordering = ["-date_envoi"]

    def __str__(self):
        return f"{self.sujet} — {self.nom}"
