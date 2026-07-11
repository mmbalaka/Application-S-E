"""Vues du site vitrine de l'association Lumière du Soleil."""
from django.contrib import messages
from django.core.mail import mail_admins
from django.shortcuts import redirect, render

from suivi.models import Coordinateur, DirecteurProjet, Indicateur, Projet, SuiviEvaluateur

from .forms import ContactForm, DemandeCompteForm

# Domaines d'intervention de l'association (cahier des charges § 1.1)
DOMAINES = [
    ("🌾", "Agriculture, élevage et pêche",
     "Appui aux producteurs, coopératives et filières locales pour une production durable."),
    ("🌍", "Environnement",
     "Protection des écosystèmes, reboisement et sensibilisation aux enjeux climatiques."),
    ("💼", "Entreprenariat",
     "Accompagnement des porteurs de projets et développement d'activités génératrices de revenus."),
    ("🎓", "Éducation, formation et recherche",
     "Accès à l'éducation, renforcement des capacités et production de connaissances."),
    ("🧒", "Protection de l'enfance",
     "Défense des droits de l'enfant et prise en charge des enfants vulnérables."),
    ("🏥", "Santé",
     "Amélioration de l'accès aux soins et prévention au bénéfice des communautés."),
]


def accueil(request):
    """Page d'accueil : message clé, chiffres, domaines, appel à l'action."""
    contexte = {
        "domaines": DOMAINES,
        "nb_projets": Projet.objects.count(),
        "nb_indicateurs": Indicateur.objects.count(),
        "nb_intervenants": (
            Coordinateur.objects.filter(actif=True).count()
            + DirecteurProjet.objects.filter(actif=True).count()
            + SuiviEvaluateur.objects.filter(actif=True).count()
        ),
    }
    return render(request, "vitrine/accueil.html", contexte)


def apropos(request):
    """Vision, mission, valeurs et équipe."""
    contexte = {
        "coordinateurs": Coordinateur.objects.filter(actif=True),
        "directeurs": DirecteurProjet.objects.filter(actif=True),
        "evaluateurs": SuiviEvaluateur.objects.filter(actif=True),
    }
    return render(request, "vitrine/apropos.html", contexte)


def services(request):
    """Domaines d'intervention et approche suivi-évaluation."""
    return render(request, "vitrine/services.html", {"domaines": DOMAINES})


def projets(request):
    """Aperçu public des projets (sans données confidentielles)."""
    return render(
        request,
        "vitrine/projets.html",
        {"projets": Projet.objects.select_related("directeur").order_by("code")},
    )


def contact(request):
    """Formulaire de contact + coordonnées."""
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Merci ! Votre message a bien été envoyé. Nous vous répondrons rapidement.",
        )
        return redirect("vitrine:contact")
    return render(request, "vitrine/contact.html", {"form": form})


def acces(request):
    """Porte d'entrée vers l'application : se connecter ou demander un compte."""
    return render(request, "vitrine/acces.html")


def demande_compte(request):
    """Demande de création de compte, soumise à l'approbation de l'administrateur."""
    form = DemandeCompteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        demande = form.save()
        # Prévenir les administrateurs (visible en console en développement)
        mail_admins(
            "Nouvelle demande de compte",
            f"{demande.nom} <{demande.email}> demande un accès à l'application.\n"
            f"Organisation : {demande.organisation or '—'}\n"
            f"Motif : {demande.motif}",
            fail_silently=True,
        )
        return render(request, "vitrine/demande_envoyee.html", {"demande": demande})
    return render(request, "vitrine/demande_compte.html", {"form": form})
