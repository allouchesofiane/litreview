from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from reviews import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Page d'accueil 
    path('', views.home_view, name='home'),
    
    # Authentification
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('feed/', views.feed_view, name='feed'),
    
]

