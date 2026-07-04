"""Interface d'administration — gestion des projets et des intervenants."""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from django.shortcuts import redirect, render
from django.urls import path

from .forms import ImportIndicateursForm
from .importation import importer_indicateurs
from .models import (
    AxeDesagregation,
    Cible,
    Coordinateur,
    DirecteurProjet,
    Indicateur,
    Projet,
    Realisation,
    SourceVerification,
    SuiviEvaluateur,
    VentilationRealisation,
)

# Couleurs du code visuel (design Lumière du Soleil)
COULEURS = {"vert": "#2f7d44", "orange": "#e8a55a", "rouge": "#c64545"}
LIBELLES_STATUT = {
    "vert": _("Atteint"),
    "orange": _("À surveiller"),
    "rouge": _("En retard"),
}


def badge(taux, seuil_vert=90, seuil_orange=70):
    """Pastille colorée « ● 95 % · Atteint » selon des seuils donnés."""
    if taux is None:
        return format_html('<span style="color:#999;">—</span>')
    if taux >= seuil_vert:
        statut = "vert"
    elif taux >= seuil_orange:
        statut = "orange"
    else:
        statut = "rouge"
    return format_html(
        '<span style="color:{};font-weight:600;">● {} %</span>'
        '<span style="color:#777;"> · {}</span>',
        COULEURS[statut],
        taux,
        LIBELLES_STATUT[statut],
    )


def badge_taux(indicateur, taux):
    """Pastille colorée selon les seuils propres à l'indicateur."""
    return badge(taux, indicateur.seuil_vert, indicateur.seuil_orange)

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
    list_display = ("nom", "email", "telephone", "nb_directeurs", "performance", "actif")
    list_filter = ("actif",)
    search_fields = ("nom", "email")
    inlines = [DirecteurInline]

    @admin.display(description=_("directeurs de projet"))
    def nb_directeurs(self, obj):
        return obj.directeurs.count()

    @admin.display(description=_("performance consolidée"))
    def performance(self, obj):
        return badge(obj.taux_moyen)


@admin.register(DirecteurProjet)
class DirecteurProjetAdmin(admin.ModelAdmin):
    list_display = ("nom", "coordinateur", "email", "nb_projets", "performance", "actif")
    list_filter = ("actif", "coordinateur")
    search_fields = ("nom", "email")
    inlines = [ProjetInline]

    @admin.display(description=_("projets"))
    def nb_projets(self, obj):
        return obj.projets.count()

    @admin.display(description=_("performance du portefeuille"))
    def performance(self, obj):
        return badge(obj.taux_moyen)


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
    list_display = ("code", "nom", "directeur", "statut", "nb_indicateurs", "performance", "date_debut", "date_fin")
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

    @admin.display(description=_("performance du projet"))
    def performance(self, obj):
        return badge(obj.taux_moyen)


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
    filter_horizontal = ("desagregations",)
    fieldsets = (
        (None, {"fields": ("projet", "code", "intitule", "definition", "niveau", "actif")}),
        (
            _("Mesure et collecte"),
            {
                "fields": (
                    "unite",
                    "frequence",
                    "type_valeur",
                    "numerateur_libelle",
                    "denominateur_libelle",
                    "mode_calcul",
                    "methode_collecte",
                    "source_donnees",
                    "moyen_verification",
                )
            },
        ),
        (_("Valeurs de référence"), {"fields": ("baseline", "cible_finale")}),
        (_("Désagrégation"), {"fields": ("desagregations",)}),
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

    # ── Import CSV / Excel ──
    def get_urls(self):
        urls = super().get_urls()
        return [
            path(
                "importer/",
                self.admin_site.admin_view(self.vue_import),
                name="suivi_indicateur_importer",
            ),
        ] + urls

    def vue_import(self, request):
        """Téléversement d'une liste d'indicateurs pour un projet."""
        form = ImportIndicateursForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            projet = form.cleaned_data["projet"]
            fichier = form.cleaned_data["fichier"]
            try:
                crees, mis_a_jour, erreurs = importer_indicateurs(
                    projet, fichier, fichier.name
                )
            except Exception as exc:  # fichier illisible, format inattendu…
                form.add_error("fichier", str(exc))
            else:
                self.message_user(
                    request,
                    _(
                        "%(projet)s : %(crees)s indicateur(s) créé(s), "
                        "%(maj)s mis à jour."
                    )
                    % {"projet": projet, "crees": crees, "maj": mis_a_jour},
                )
                for erreur in erreurs:
                    self.message_user(request, erreur, level="WARNING")
                return redirect("..")
        contexte = {
            **self.admin_site.each_context(request),
            "form": form,
            "title": _("Importer des indicateurs"),
            "opts": self.model._meta,
        }
        return render(request, "admin/suivi/indicateur/importer.html", contexte)

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


class VentilationInline(admin.TabularInline):
    """Ventilation de la réalisation par axe (sexe, âge, zone…)."""

    model = VentilationRealisation
    extra = 0


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = (
        "indicateur",
        "periode_affichee",
        "valeur",
        "cible_periode",
        "taux_affiche",
        "total_ventile",
        "nb_sources",
    )
    list_filter = ("indicateur__projet", "annee")
    search_fields = ("indicateur__intitule", "indicateur__code", "commentaire")
    inlines = [VentilationInline, SourceInline]
    fields = (
        "indicateur",
        "annee",
        "periode",
        "valeur",
        "numerateur",
        "denominateur",
        "commentaire",
    )

    @admin.display(description=_("total ventilé"))
    def total_ventile(self, obj):
        total = obj.somme_ventilations
        if total is None:
            return "—"
        if obj.valeur is not None and total != obj.valeur:
            return format_html(
                '<span style="color:#c64545;" title="{}">{} ⚠</span>',
                _("Différent de la valeur réalisée"),
                total,
            )
        return total

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


@admin.register(AxeDesagregation)
class AxeDesagregationAdmin(admin.ModelAdmin):
    list_display = ("nom", "modalites", "nb_indicateurs")
    search_fields = ("nom",)

    @admin.display(description=_("indicateurs concernés"))
    def nb_indicateurs(self, obj):
        return obj.indicateurs.count()
