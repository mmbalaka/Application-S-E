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


# ══════════════════════════════════════════════════════════════
#  Cœur du S&E : indicateurs, cibles, réalisations, sources
# ══════════════════════════════════════════════════════════════


class Indicateur(models.Model):
    """Indicateur de performance rattaché à un projet."""

    class Niveau(models.TextChoices):
        IMPACT = "impact", _("Impact")
        EFFET = "effet", _("Effet")
        PRODUIT = "produit", _("Produit")

    class Frequence(models.TextChoices):
        MENSUELLE = "mensuelle", _("Mensuelle")
        TRIMESTRIELLE = "trimestrielle", _("Trimestrielle")
        SEMESTRIELLE = "semestrielle", _("Semestrielle")
        ANNUELLE = "annuelle", _("Annuelle")

    projet = models.ForeignKey(
        Projet,
        verbose_name=_("projet"),
        related_name="indicateurs",
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        _("code"),
        max_length=30,
        blank=True,
        help_text=_("Référence courte de l'indicateur (ex. : IND-01)."),
    )
    intitule = models.CharField(_("intitulé"), max_length=250)
    definition = models.TextField(_("définition"), blank=True)
    unite = models.CharField(
        _("unité"),
        max_length=50,
        help_text=_("Ex. : personnes, hectares, tonnes, %…"),
    )
    niveau = models.CharField(
        _("niveau"), max_length=10, choices=Niveau.choices, default=Niveau.PRODUIT
    )
    mode_calcul = models.TextField(_("mode de calcul"), blank=True)
    methode_collecte = models.CharField(_("méthode de collecte"), max_length=200, blank=True)
    source_donnees = models.CharField(_("source des données"), max_length=200, blank=True)
    frequence = models.CharField(
        _("fréquence de collecte"),
        max_length=15,
        choices=Frequence.choices,
        default=Frequence.TRIMESTRIELLE,
    )
    baseline = models.DecimalField(
        _("valeur de référence (baseline)"),
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )
    cible_finale = models.DecimalField(
        _("cible finale"), max_digits=14, decimal_places=2, null=True, blank=True
    )
    # Seuils paramétrables du code couleur (cahier des charges § 3.2)
    seuil_vert = models.PositiveSmallIntegerField(
        _("seuil vert (%)"),
        default=90,
        help_text=_("Taux à partir duquel l'indicateur est « Atteint »."),
    )
    seuil_orange = models.PositiveSmallIntegerField(
        _("seuil orange (%)"),
        default=70,
        help_text=_("Taux à partir duquel l'indicateur est « À surveiller »."),
    )
    actif = models.BooleanField(_("actif"), default=True)

    class Meta:
        verbose_name = _("indicateur")
        verbose_name_plural = _("indicateurs")
        ordering = ["projet", "code", "intitule"]

    def __str__(self):
        prefixe = f"{self.code} — " if self.code else ""
        return f"{prefixe}{self.intitule}"

    # ── Nombre de périodes par an selon la fréquence ──
    PERIODES_PAR_AN = {
        Frequence.MENSUELLE: 12,
        Frequence.TRIMESTRIELLE: 4,
        Frequence.SEMESTRIELLE: 2,
        Frequence.ANNUELLE: 1,
    }

    @property
    def cumul_realise(self):
        """Somme de toutes les valeurs réalisées."""
        return self.realisations.aggregate(total=models.Sum("valeur"))["total"]

    @property
    def taux_final(self):
        """Taux de réalisation cumulé vs cible finale : (cumul ÷ cible finale) × 100."""
        cumul = self.cumul_realise
        if cumul is None or not self.cible_finale:
            return None
        return round(float(cumul) / float(self.cible_finale) * 100)

    def statut_pour(self, taux):
        """Code couleur selon les seuils paramétrés : vert / orange / rouge."""
        if taux is None:
            return None
        if taux >= self.seuil_vert:
            return "vert"
        if taux >= self.seuil_orange:
            return "orange"
        return "rouge"


class MesurePeriodique(models.Model):
    """Champs communs aux cibles et réalisations (une valeur par période)."""

    indicateur = models.ForeignKey(
        Indicateur,
        verbose_name=_("indicateur"),
        related_name="%(class)ss",
        on_delete=models.CASCADE,
    )
    annee = models.PositiveSmallIntegerField(_("année"))
    periode = models.PositiveSmallIntegerField(
        _("numéro de période"),
        default=1,
        help_text=_(
            "Selon la fréquence de l'indicateur : mois (1-12), trimestre (1-4), "
            "semestre (1-2) ou 1 si annuelle."
        ),
    )

    class Meta:
        abstract = True
        ordering = ["annee", "periode"]

    PREFIXES = {
        Indicateur.Frequence.MENSUELLE: "M",
        Indicateur.Frequence.TRIMESTRIELLE: "T",
        Indicateur.Frequence.SEMESTRIELLE: "S",
        Indicateur.Frequence.ANNUELLE: "",
    }

    @property
    def periode_str(self):
        """Libellé lisible de la période, ex. « T2 2026 »."""
        prefixe = self.PREFIXES.get(self.indicateur.frequence, "")
        if not prefixe:
            return str(self.annee)
        return f"{prefixe}{self.periode} {self.annee}"

    def __str__(self):
        return f"{self.indicateur} · {self.periode_str}"


class Cible(MesurePeriodique):
    """Valeur cible attendue pour un indicateur sur une période."""

    valeur = models.DecimalField(_("valeur cible"), max_digits=14, decimal_places=2)

    class Meta(MesurePeriodique.Meta):
        verbose_name = _("cible")
        verbose_name_plural = _("cibles")
        constraints = [
            models.UniqueConstraint(
                fields=["indicateur", "annee", "periode"],
                name="cible_unique_par_periode",
            )
        ]


class Realisation(MesurePeriodique):
    """Valeur réellement atteinte pour un indicateur sur une période."""

    valeur = models.DecimalField(_("valeur réalisée"), max_digits=14, decimal_places=2)
    commentaire = models.TextField(_("commentaire"), blank=True)
    date_saisie = models.DateTimeField(_("date de saisie"), auto_now_add=True)

    class Meta(MesurePeriodique.Meta):
        verbose_name = _("réalisation")
        verbose_name_plural = _("réalisations")
        constraints = [
            models.UniqueConstraint(
                fields=["indicateur", "annee", "periode"],
                name="realisation_unique_par_periode",
            )
        ]

    @property
    def cible_correspondante(self):
        """La cible définie pour le même indicateur et la même période."""
        return Cible.objects.filter(
            indicateur=self.indicateur, annee=self.annee, periode=self.periode
        ).first()

    @property
    def taux(self):
        """Taux de réalisation périodique : (réalisé ÷ cible période) × 100."""
        cible = self.cible_correspondante
        if cible is None or not cible.valeur:
            return None
        return round(float(self.valeur) / float(cible.valeur) * 100)

    @property
    def ecart_absolu(self):
        """Écart absolu : réalisé − cible."""
        cible = self.cible_correspondante
        if cible is None:
            return None
        return self.valeur - cible.valeur

    @property
    def ecart_relatif(self):
        """Écart relatif : (écart ÷ cible) × 100."""
        cible = self.cible_correspondante
        if cible is None or not cible.valeur:
            return None
        return round(float(self.ecart_absolu) / float(cible.valeur) * 100)

    @property
    def statut(self):
        """Code couleur de la période : vert / orange / rouge."""
        return self.indicateur.statut_pour(self.taux)


class SourceVerification(models.Model):
    """Justificatif (fichier) rattaché à une réalisation."""

    realisation = models.ForeignKey(
        Realisation,
        verbose_name=_("réalisation"),
        related_name="sources",
        on_delete=models.CASCADE,
    )
    titre = models.CharField(_("titre"), max_length=200)
    fichier = models.FileField(_("fichier"), upload_to="sources/%Y/")
    date_ajout = models.DateTimeField(_("date d'ajout"), auto_now_add=True)

    class Meta:
        verbose_name = _("source de vérification")
        verbose_name_plural = _("sources de vérification")
        ordering = ["-date_ajout"]

    def __str__(self):
        return self.titre
