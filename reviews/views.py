from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import (SignUpForm, LoginForm)

User = get_user_model()

# Vue page d'acceuil
def home_view(request):
    """
    Page d'accueil pour les utilisateurs non connectés.
    """
    form = LoginForm(request.POST)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('feed')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

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
                messages.success(request, f"Bienvenue {username} !")
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
    Vue pour la déconnexion d'un utilisateur.
    """
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')


# VUE PRINCIPALE
@login_required
def feed_view(request):
    return render(request, "reviews/feed.html", {"posts": []})

