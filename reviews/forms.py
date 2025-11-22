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


class TicketForm(forms.ModelForm):
    """
    Formulaire pour créer/modifier un ticket (demande de critique).
    """
    title = forms.CharField(
        max_length=150,
        required=True,
        label="Titre"
    )
    
    description = forms.CharField(
        max_length=2000,
        required=False,
        label="Description"
    )
    
    image = forms.ImageField(
        required=False,
        label="Image"
    )

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer/modifier une critique.
    """
    RATING_CHOICES = [(i, '★' * i) for i in range(6)]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        required=True,
        label="Note"
    )
    
    headline = forms.CharField(
        max_length=100,
        required=True,
        label="Titre"
    )
    
    body = forms.CharField(
        max_length=7000,
        required=False,
        label="Commentaire"
    )

    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']

class TicketReviewForm(forms.Form):
    """
    Formulaire combiné pour créer un ticket ET une critique en une seule étape.
    """
    # Champs du Ticket
    ticket_title = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}),
        label="Titre du livre/article"
    )
    
    ticket_description = forms.CharField(max_length=2048, required=False, widget=forms.Textarea(attrs={'class': 'form-textarea','rows': 3}),
        label="Description"
    )
    
    ticket_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-file-input','accept': 'image/*'}),
        label="Image"
    )
    
    # Champs de la Review
    RATING_CHOICES = [(i, '★' * i) for i in range(6)]
    
    rating = forms.ChoiceField(choices=RATING_CHOICES,required=True, widget=forms.RadioSelect(attrs={'class': 'rating-input'}),
        label="Note"
    )
    
    headline = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}),
        label="Titre de la critique"
    )
    
    body = forms.CharField(max_length=8192, required=False, widget=forms.Textarea(attrs={'class': 'form-textarea','rows': 8}),
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
        widget=forms.TextInput(attrs={'class': 'form-input', 'autofocus': True}),
        label="Nom d'utilisateur"
    )

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        """Valide le nom d'utilisateur à suivre"""
        username = self.cleaned_data.get('username')
        
        # Vérifier que l'utilisateur existe
        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f"L'utilisateur '{username}' n'existe pas.")
        
        # Empêcher de se suivre soi-même
        if self.current_user and user_to_follow == self.current_user:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.")
        
        # Vérifier si l'abonnement existe déjà
        if self.current_user and UserFollows.objects.filter(
            user=self.current_user,
            followed_user=user_to_follow
        ).exists():
            raise forms.ValidationError(f"Vous suivez déjà {username}.")
        
        return username


class DeleteConfirmForm(forms.Form):
    """
    Formulaire simple pour confirmer la suppression.
    """
    confirm = forms.BooleanField(required=True, widget=forms.HiddenInput(), initial=True)

