from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    """
    Formulaire de connexion.
    """
    username = forms.CharField(
        max_length=100,
        required=True,
        label="Nom d'utilisateur"
    )
    
    password = forms.CharField(
        required=True,
        label="Mot de passe"
    )
class SignUpForm(UserCreationForm):
    """
    Formulaire d'inscription utilisateur,Hérite de UserCreationForm pour gérer le mot de pass 1 et le mot de passe 2.
    """
    username = forms.CharField(
        max_length=100,
        required=True,
        label="Nom d'utilisateur"
    )
    
    password1 = forms.CharField(
        required=True,
        label="Mot de passe"
    )
    
    password2 = forms.CharField(
        required=True,
        label="Confirmer mot de passe"
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


