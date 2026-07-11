"""Administration du site vitrine : approbation des demandes de compte."""
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .models import DemandeCompte, MessageContact


@admin.register(DemandeCompte)
class DemandeCompteAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "organisation", "fonction", "statut", "date_demande")
    list_filter = ("statut",)
    search_fields = ("nom", "email", "organisation")
    readonly_fields = ("date_demande", "date_traitement")
    actions = ["approuver", "refuser"]

    @admin.action(description=_("Approuver et créer le compte"))
    def approuver(self, request, queryset):
        for demande in queryset.filter(statut=DemandeCompte.Statut.EN_ATTENTE):
            if User.objects.filter(username=demande.email).exists():
                self.message_user(
                    request,
                    _("%(email)s : un compte existe déjà.") % {"email": demande.email},
                    level="WARNING",
                )
                continue
            mot_de_passe = get_random_string(10)
            User.objects.create_user(
                username=demande.email,
                email=demande.email,
                password=mot_de_passe,
                first_name=demande.nom[:150],
                is_staff=False,
            )
            demande.statut = DemandeCompte.Statut.APPROUVEE
            demande.date_traitement = timezone.now()
            demande.save()
            send_mail(
                "Votre accès à l'application Lumière du Soleil",
                (
                    f"Bonjour {demande.nom},\n\n"
                    "Votre demande d'accès à l'application de suivi-évaluation "
                    "a été approuvée.\n\n"
                    f"Identifiant : {demande.email}\n"
                    f"Mot de passe provisoire : {mot_de_passe}\n\n"
                    "Merci de changer ce mot de passe dès votre première connexion.\n\n"
                    "L'équipe Lumière du Soleil"
                ),
                None,
                [demande.email],
                fail_silently=True,
            )
            self.message_user(
                request,
                _(
                    "Compte créé pour %(email)s — mot de passe provisoire : %(mdp)s "
                    "(communiquez-le à l'utilisateur, il n'apparaîtra plus)."
                )
                % {"email": demande.email, "mdp": mot_de_passe},
            )

    @admin.action(description=_("Refuser la demande"))
    def refuser(self, request, queryset):
        nb = queryset.filter(statut=DemandeCompte.Statut.EN_ATTENTE).update(
            statut=DemandeCompte.Statut.REFUSEE, date_traitement=timezone.now()
        )
        if nb:
            self.message_user(request, _("%(nb)s demande(s) refusée(s).") % {"nb": nb})


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ("sujet", "nom", "email", "date_envoi", "traite")
    list_filter = ("traite",)
    search_fields = ("sujet", "nom", "email", "message")
    readonly_fields = ("nom", "email", "sujet", "message", "date_envoi")
    list_editable = ("traite",)
