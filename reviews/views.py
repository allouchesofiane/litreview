from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import (SignUpForm, LoginForm, TicketForm, ReviewForm, TicketReviewForm, FollowUserForm)
from .models import Ticket, Review, UserFollows
from django.db.models import Value, CharField
from django.db.models import Exists, OuterRef


User = get_user_model()

# Vue page d'acceuil
def home_view(request):
    """
    Page d'accueil pour les utilisateurs non connectés.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, 'reviews/home.html', {'form': form})

# Vue page d'inscription
def signup_view(request):
    """
    Vue pour l'inscription d'un nouvel utilisateur.
    """

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Votre compte a été créé avec succès.")
            return redirect('home')
        else:
            messages.error(request, "Erreur lors de l'inscription. Veuillez corriger les erreurs.")
    else:
        form = SignUpForm()
    
    return render(request, 'reviews/signup.html', {'form': form})

# Vue pour la connexion

def login_view(request):
    """
    Vue pour la connexion d'un utilisateur.
    """
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    
    return render(request, 'reviews/login.html', {'form': form})

# Vue pour la deconnexion
@login_required
def logout_view(request):
    """
    Vue pour la déconnexion .
    """
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('home')


@login_required
def feed_view(request):

    tickets = Ticket.objects.annotate(
        content_type=Value('TICKET', output_field=CharField()),
        already_reviewed=Exists(
            Review.objects.filter(ticket=OuterRef('pk'), user=request.user)
        )
    )

    reviews = Review.objects.annotate(
        content_type=Value('REVIEW', output_field=CharField())
    )

    posts = list(tickets) + list(reviews)
    posts.sort(key=lambda p: p.time_created, reverse=True)

    return render(request, "reviews/feed.html", {"posts": posts})


@login_required
def create_ticket_view(request):
    """
    Vue pour créer un nouveau ticket (demande de critique).
    """
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Votre ticket a été créé avec succès !")
            return redirect('feed')
        else:
            messages.error(request, "Erreur lors de la création du ticket.")
    else:
        form = TicketForm()
    
    return render(request, 'reviews/create_ticket.html', {'form': form})

@login_required
def create_review_view(request, ticket_id):
    """
    Vue pour créer une review en réponse à un ticket existant.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Vérifier si l'utilisateur a déjà répondu à ce ticket
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        return redirect('feed')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "Votre critique a été publiée avec succès !")
            return redirect('feed')
        else:
            messages.error(request, "Erreur lors de la création de la critique.")
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/create_review.html', {'form': form, 'ticket': ticket})

@login_required
def edit_ticket_view(request, ticket_id):
    """
    Vue pour modifier un ticket existant.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre ticket a été modifié avec succès !")
            return redirect('posts')
        else:
            messages.error(request, "Erreur lors de la modification du ticket.")
    else:
        form = TicketForm(instance=ticket)
    
    return render(request, 'reviews/edit_ticket.html', {'form': form, 'ticket': ticket})


@login_required
def delete_ticket_view(request, ticket_id):
    """
    Vue pour supprimer un ticket (seulement l'auteur).
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Votre ticket a été supprimé avec succès !")
        return redirect('posts')
    
    return render(request, 'reviews/delete_ticket.html', {'ticket': ticket})


@login_required
def create_ticket_review_view(request):
    """
    Vue pour créer un ticket et une review en même temps.
    """
    if request.method == 'POST':
        form = TicketReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Créer le ticket dans la base 
            ticket = Ticket.objects.create(
                title=form.cleaned_data['ticket_title'],
                description=form.cleaned_data['ticket_description'],
                image=form.cleaned_data['ticket_image'],
                user=request.user
            )
            
            # Créer la review associée
            Review.objects.create(
                ticket=ticket,
                rating=form.cleaned_data['rating'],
                headline=form.cleaned_data['headline'],
                body=form.cleaned_data['body'],
                user=request.user
            )
            
            messages.success(request, "Votre critique a été créée avec succès !")
            return redirect('feed')
        else:
            messages.error(request, "Erreur lors de la création de la critique.")
    else:
        form = TicketReviewForm()
    
    return render(request, 'reviews/create_ticket_review.html', {'form': form})


@login_required
def edit_review_view(request, review_id):
    """
    Vue pour modifier une review existante (seulement l'auteur).
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre critique a été modifiée avec succès !")
            return redirect('posts')
        else:
            messages.error(request, "Erreur lors de la modification de la critique.")
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})


@login_required
def delete_review_view(request, review_id):
    """
    Vue pour supprimer une review (seulement l'auteur).
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Votre critique a été supprimée avec succès !")
        return redirect('posts')
    
    return render(request, 'reviews/delete_review.html', {'review': review})



@login_required
def posts_view(request):
    """
    Vue pour afficher tous les posts de l'utilisateur .
    """
    tickets = Ticket.objects.filter(user=request.user).annotate(
        content_type=Value('TICKET', CharField())
    )

    reviews = Review.objects.filter(user=request.user).annotate(
        content_type=Value('REVIEW', CharField())
    )

    # Combiner les requettes
    posts = list(tickets) + list(reviews)

    # Trier par ordre 
    posts.sort(key=lambda post: post.time_created, reverse=True)

    return render(request, 'reviews/posts.html', {'posts': posts})


@login_required
def subscriptions_view(request):
    """
    Vue pour gérer les abonnements (suivre/ne plus suivre des utilisateurs).
    """
    # Traiter le formulaire de suivi
    if request.method == 'POST':
        form = FollowUserForm(request.POST, current_user=request.user)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_to_follow = User.objects.get(username=username)
            UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
            messages.success(request, f"Vous suivez maintenant {username}.")
            return redirect('subscriptions')
        else:
            # Les erreurs sont déjà gérées par le formulaire
            pass
    else:
        form = FollowUserForm(current_user=request.user)
    
    # Récupérer les abonnements (utilisateurs suivis)
    following = UserFollows.objects.filter(user=request.user).select_related('followed_user')
    
    # Récupérer les abonnés (utilisateurs qui me suivent)
    followers = UserFollows.objects.filter(followed_user=request.user).select_related('user')
    
    context = {
        'form': form,
        'following': following,
        'followers': followers
    }
    
    return render(request, 'reviews/subscriptions.html', context)


@login_required
def unfollow_user_view(request, user_id):
    """
    Vue pour ne plus suivre un utilisateur.
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow = get_object_or_404(UserFollows, user=request.user, followed_user=user_to_unfollow)
    
    if request.method == 'POST':
        follow.delete()
        messages.success(request, f"Vous ne suivez plus {user_to_unfollow.username}.")
        return redirect('subscriptions')
    
    return render(request, 'reviews/unfollow_confirm.html', {'user_to_unfollow': user_to_unfollow})


