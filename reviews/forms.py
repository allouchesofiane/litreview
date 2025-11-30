from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Ticket, Review, UserFollows

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
        label="Mot de passe",
        widget=forms.PasswordInput()
    )


class SignUpForm(UserCreationForm):
    """
    Formulaire d'inscription utilisateur,
    Hérite de UserCreationForm pour gérer le mot de pass 1
    et le mot de passe 2.
    """
    username = forms.CharField(
        max_length=100,
        required=True,
        label="Nom d'utilisateur"
    )

    password1 = forms.CharField(
        required=True,
        label="Mot de passe",
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        required=True,
        label="Confirmer mot de passe",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer/modifier un ticket (demande de critique).
    """

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer/modifier une critique.
    """
    RATING_CHOICES = [
        (i, '★' * i if i > 0 else 'Aucune note') for i in range(6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Note"
    )

    body = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 8,
            'class': 'form-control'
        }),
        required=False,
        label="Commentaire"
    )

    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TicketReviewForm(forms.Form):
    """
    Formulaire combiné pour créer un ticket et une critique en une seule étape.
    """
    # Champs du Ticket
    ticket_title = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Titre du livre ou de l’article'
        }),
        label="Titre du livre/article"
    )

    ticket_description = forms.CharField(
        max_length=2048,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Décrivez brièvement le contenu…'
        }),
        label="Description"
    )

    ticket_image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label="Image"
    )

    # Champs de la Review
    RATING_CHOICES = [
        (i, '★' * i if i > 0 else 'Aucune note') for i in range(6)
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        required=True,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label="Note"
    )

    headline = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Titre de votre critique'
        }),
        label="Titre de la critique"
    )

    body = forms.CharField(
        max_length=8192,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Votre avis sur le livre / article…'
        }),
        label="Commentaire"
    )

    def clean_rating(self):
        """Convertit le rating en entier"""
        rating = self.cleaned_data.get('rating')
        return int(rating)


class FollowUserForm(forms.Form):
    """
    Formulaire pour suivre un utilisateur.
    L'utilisateur entre le nom d'utilisateur à suivre.
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input', 'autofocus': True}),
        label="Nom d'utilisateur"
    )

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop(
            'current_user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        """Valide le nom d'utilisateur à suivre"""
        username = self.cleaned_data.get('username')

        # Vérifier que l'utilisateur existe
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(
                f"L'utilisateur '{username}' n'existe pas.")

        # Empêcher de se suivre soi-même
        if self.current_user and user_to_follow == self.current_user:
            raise forms.ValidationError(
                "Vous ne pouvez pas vous suivre vous-même.")

        # Vérifier si l'abonnement existe déjà
        if self.current_user and UserFollows.objects.filter(
            user=self.current_user,
            followed_user=user_to_follow
        ).exists():
            raise forms.ValidationError(
                f"Vous suivez déjà {username}.")

        return username


class DeleteConfirmForm(forms.Form):
    """
    Formulaire simple pour confirmer la suppression.
    """
    confirm = forms.BooleanField(
        required=True,
        widget=forms.HiddenInput(),
        initial=True)
