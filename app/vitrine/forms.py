"""Formulaires du site vitrine."""
from django import forms

from .models import DemandeCompte, MessageContact


class DemandeCompteForm(forms.ModelForm):
    class Meta:
        model = DemandeCompte
        fields = ["nom", "email", "organisation", "fonction", "motif"]
        widgets = {
            "nom": forms.TextInput(attrs={"placeholder": "Votre nom complet"}),
            "email": forms.EmailInput(attrs={"placeholder": "vous@exemple.org"}),
            "organisation": forms.TextInput(
                attrs={"placeholder": "Votre organisation (facultatif)"}
            ),
            "fonction": forms.TextInput(
                attrs={"placeholder": "Votre fonction (facultatif)"}
            ),
            "motif": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Expliquez brièvement pourquoi vous souhaitez accéder à l'application.",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if DemandeCompte.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Une demande existe déjà pour cette adresse e-mail. "
                "Elle est en cours de traitement."
            )
        return email


class ContactForm(forms.ModelForm):
    class Meta:
        model = MessageContact
        fields = ["nom", "email", "sujet", "message"]
        widgets = {
            "nom": forms.TextInput(attrs={"placeholder": "Votre nom"}),
            "email": forms.EmailInput(attrs={"placeholder": "vous@exemple.org"}),
            "sujet": forms.TextInput(attrs={"placeholder": "Objet de votre message"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Votre message…"}),
        }
