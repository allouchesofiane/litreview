from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    """
    
    class Meta:
        verbose_name = "Utilisateur"
    
    def __str__(self):
        return self.username

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

    def user_has_reviewed(self, user):
        """Vérifie si l'utilisateur a déjà créé une critique pour ce ticket"""
        return self.review_set.filter(user=user).exists()

    class Meta:
        ordering = ['-time_created']
        verbose_name = "Ticket"

class Review(models.Model):
    """
    Modèle représentant une critique de livre/article.
    """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, verbose_name="Ticket associé")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note")
    headline = models.CharField(max_length=128, verbose_name="Titre de la critique")
    body = models.CharField(max_length=8192, blank=True, verbose_name="Commentaire")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Auteur")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de la création")

    class Meta:
        ordering = ['-time_created']
        verbose_name = "Critique"

class UserFollows(models.Model):
    """
    Modèle représentant la relation de suivi entre utilisateurs.
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name="Utilisateur"
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by',
        verbose_name="Utilisateur suivi"
    )

    class Meta:
        # Empêche qu'un utilisateur suive la même personne plusieurs fois
        unique_together = ('user', 'followed_user')
        verbose_name = "Abonnement"

    def __str__(self):
        return f"{self.user.username} suit {self.followed_user.username}"

    

    
# class Book(models.Model):
#     ADVENTURE = "AV"
#     THRILLER = "TR"
#     FANTASY = "FS"
#     ROMANCE = "RM"
#     HORROR = "HR"
#     SCIENCE_FICTION = "SF"
#     GENRES = [
#         (ADVENTURE, "Aventure"),
#         (THRILLER, "Thriller"),
#         (FANTASY, "Fantastique"),
#         (ROMANCE, "Romance"),
#         (HORROR, "Horreur"),
#         (SCIENCE_FICTION, "Science-fiction"),]
#     title = models.CharField(max_length=100)
#     price = models.FloatField(max_digits=10)
#     summary = models.TextField(max_length=200)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.CharField(max_length=25, choices="GENRES")
#     stock = models.IntegerField(default=0)

#     def __str__(self):
#         return self.title

# class Author(models.Model):
#     firstname=models.CharField(max_length=100)
#     lastname=models.CharField(max_length=100)
#     wikipedia=models.CharField(max_length=100)

#     def __str__(self):
#         return "f mon nom est {self.firstname} et mon prenom est {self.lastname}"