from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):

    """
    Modèle représentant une demande de critique (billet).
    Un utilisateur crée un ticket pour demander des avis sur un livre/article.
    """

    title = models.CharField(max_length=128, verbose_name="Titre")
    description =models.TextField(max_length=2048,blank=True, verbose_name="Description")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="Auteur")
    image = models.ImageField(null=True, blank=True, verbose_name="Image")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        ordering = ['-time_created']
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

class Review(models.Model):
    """
    Modèle représentant une critique de livre/article.
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, verbose_name="Ticket associé")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note")
    headline = models.CharField(max_length=128, verbose_name="Titre de la critique")
    body = models.CharField(max_length=8192, blank=True, verbose_name="Commentaire")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Auteur")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Datede la création")

    class Meta:
        ordering = ['-time_created']
        verbose_name = "Critique"
        verbose_name_plural = "Critiques"


class UserFollows(models.Model):

    """
    Modèle représentant la relation de suivi entre utilisateurs.
    Un utilisateur (user) suit un autre utilisateur (followed_user).
    """
    # Your UserFollows model definition goes here
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following', verbose_name="Utilisateur")
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by', verbose_name="Utilisateur suivi")


    class Meta:
        # Empêche qu'un utilisateur suive la même personne plusieurs fois
        unique_together = ('user', 'followed_user')
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"