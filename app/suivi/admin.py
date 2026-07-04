"""Interface d'administration — gestion des projets et des intervenants."""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    Cible,
    Coordinateur,
    DirecteurProjet,
    Indicateur,
    Projet,
    Realisation,
    SourceVerification,
    SuiviEvaluateur,
)

# Couleurs du code visuel (design Lumière du Soleil)
COULEURS = {"vert": "#2f7d44", "orange": "#e8a55a", "rouge": "#c64545"}
LIBELLES_STATUT = {
    "vert": _("Atteint"),
    "orange": _("À surveiller"),
    "rouge": _("En retard"),
}


def badge_taux(indicateur, taux):
    """Pastille colorée « 95 % » selon les seuils de l'indicateur."""
    if taux is None:
        return format_html('<span style="color:#999;">—</span>')
    statut = indicateur.statut_pour(taux)
    return format_html(
        '<span style="color:{};font-weight:600;">● {} %</span>'
        '<span style="color:#777;"> · {}</span>',
        COULEURS[statut],
        taux,
        LIBELLES_STATUT[statut],
    )

# En-têtes de l'admin
admin.site.site_header = _("Lumière du Soleil — Administration S&E")
admin.site.site_title = _("Admin S&E")
admin.site.index_title = _("Gestion du suivi-évaluation")


class DirecteurInline(admin.TabularInline):
    """Directeurs listés directement dans la fiche du coordinateur."""

    model = DirecteurProjet
    extra = 0
    fields = ("nom", "email", "telephone", "actif")


class ProjetInline(admin.TabularInline):
    """Projets listés directement dans la fiche du directeur."""

    model = Projet
    extra = 0
    fields = ("code", "nom", "statut", "date_debut", "date_fin")
    show_change_link = True


@admin.register(Coordinateur)
class CoordinateurAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "telephone", "nb_directeurs", "actif")
    list_filter = ("actif",)
    search_fields = ("nom", "email")
    inlines = [DirecteurInline]

    @admin.display(description=_("directeurs de projet"))
    def nb_directeurs(self, obj):
        return obj.directeurs.count()


@admin.register(DirecteurProjet)
class DirecteurProjetAdmin(admin.ModelAdmin):
    list_display = ("nom", "coordinateur", "email", "nb_projets", "actif")
    list_filter = ("actif", "coordinateur")
    search_fields = ("nom", "email")
    inlines = [ProjetInline]

    @admin.display(description=_("projets"))
    def nb_projets(self, obj):
        return obj.projets.count()


@admin.register(SuiviEvaluateur)
class SuiviEvaluateurAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "telephone", "nb_projets", "actif")
    list_filter = ("actif",)
    search_fields = ("nom", "email")

    @admin.display(description=_("projets suivis"))
    def nb_projets(self, obj):
        return obj.projets.count()


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ("code", "nom", "directeur", "statut", "nb_indicateurs", "date_debut", "date_fin")
    list_filter = ("statut", "directeur", "suivi_evaluateurs")
    search_fields = ("code", "nom", "description")
    filter_horizontal = ("suivi_evaluateurs",)
    fieldsets = (
        (None, {"fields": ("code", "nom", "description", "domaine", "statut")}),
        (_("Calendrier"), {"fields": ("date_debut", "date_fin")}),
        (_("Responsables"), {"fields": ("directeur", "suivi_evaluateurs")}),
    )

    @admin.display(description=_("indicateurs"))
    def nb_indicateurs(self, obj):
        return obj.indicateurs.count()


# ══════════════════════════════════════════════════════════════
#  Indicateurs, cibles, réalisations, sources de vérification
# ══════════════════════════════════════════════════════════════


class CibleInline(admin.TabularInline):
    model = Cible
    extra = 0


class RealisationInline(admin.TabularInline):
    model = Realisation
    extra = 0
    fields = ("annee", "periode", "valeur", "commentaire")
    show_change_link = True


@admin.register(Indicateur)
class IndicateurAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "intitule",
        "projet",
        "niveau",
        "unite",
        "cible_finale",
        "cumul",
        "taux_cumule",
        "actif",
    )
    list_filter = ("projet", "niveau", "frequence", "actif")
    search_fields = ("code", "intitule", "definition")
    inlines = [CibleInline, RealisationInline]
    fieldsets = (
        (None, {"fields": ("projet", "code", "intitule", "definition", "niveau", "actif")}),
        (
            _("Mesure et collecte"),
            {"fields": ("unite", "frequence", "mode_calcul", "methode_collecte", "source_donnees")},
        ),
        (_("Valeurs de référence"), {"fields": ("baseline", "cible_finale")}),
        (
            _("Seuils du code couleur"),
            {
                "fields": ("seuil_vert", "seuil_orange"),
                "description": _(
                    "Vert : taux ≥ seuil vert · Orange : taux ≥ seuil orange · Rouge : en dessous."
                ),
            },
        ),
    )

    @admin.display(description=_("cumul réalisé"))
    def cumul(self, obj):
        return obj.cumul_realise if obj.cumul_realise is not None else "—"

    @admin.display(description=_("taux cumulé"))
    def taux_cumule(self, obj):
        return badge_taux(obj, obj.taux_final)


class SourceInline(admin.TabularInline):
    model = SourceVerification
    extra = 0
    fields = ("titre", "fichier")


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = (
        "indicateur",
        "periode_affichee",
        "valeur",
        "cible_periode",
        "taux_affiche",
        "nb_sources",
    )
    list_filter = ("indicateur__projet", "annee")
    search_fields = ("indicateur__intitule", "indicateur__code", "commentaire")
    inlines = [SourceInline]

    @admin.display(description=_("période"))
    def periode_affichee(self, obj):
        return obj.periode_str

    @admin.display(description=_("cible période"))
    def cible_periode(self, obj):
        cible = obj.cible_correspondante
        return cible.valeur if cible else "—"

    @admin.display(description=_("taux de réalisation"))
    def taux_affiche(self, obj):
        return badge_taux(obj.indicateur, obj.taux)

    @admin.display(description=_("sources"))
    def nb_sources(self, obj):
        return obj.sources.count()


@admin.register(Cible)
class CibleAdmin(admin.ModelAdmin):
    list_display = ("indicateur", "periode_affichee", "valeur")
    list_filter = ("indicateur__projet", "annee")
    search_fields = ("indicateur__intitule", "indicateur__code")

    @admin.display(description=_("période"))
    def periode_affichee(self, obj):
        return obj.periode_str


@admin.register(SourceVerification)
class SourceVerificationAdmin(admin.ModelAdmin):
    list_display = ("titre", "realisation", "date_ajout")
    search_fields = ("titre",)
    list_filter = ("date_ajout",)
