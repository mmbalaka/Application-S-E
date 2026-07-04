"""Interface d'administration — gestion des projets et des intervenants."""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Coordinateur, DirecteurProjet, Projet, SuiviEvaluateur

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
    list_display = ("code", "nom", "directeur", "statut", "date_debut", "date_fin")
    list_filter = ("statut", "directeur", "suivi_evaluateurs")
    search_fields = ("code", "nom", "description")
    filter_horizontal = ("suivi_evaluateurs",)
    fieldsets = (
        (None, {"fields": ("code", "nom", "description", "domaine", "statut")}),
        (_("Calendrier"), {"fields": ("date_debut", "date_fin")}),
        (_("Responsables"), {"fields": ("directeur", "suivi_evaluateurs")}),
    )
