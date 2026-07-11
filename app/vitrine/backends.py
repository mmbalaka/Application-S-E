"""Connexion par identifiant OU adresse e-mail."""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class IdentifiantOuEmailBackend(ModelBackend):
    """Permet de se connecter avec le nom d'utilisateur ou l'adresse e-mail."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None or password is None:
            return None
        try:
            utilisateur = (
                UserModel.objects.filter(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
                .order_by("id")
                .first()
            )
        except Exception:
            return None
        if utilisateur is None:
            # Égalise le temps de réponse (bonne pratique de sécurité)
            UserModel().set_password(password)
            return None
        if utilisateur.check_password(password) and self.user_can_authenticate(utilisateur):
            return utilisateur
        return None
