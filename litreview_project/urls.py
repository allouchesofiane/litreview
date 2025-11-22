from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from reviews import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentification
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Flux
    path('feed/', views.feed_view, name='feed'),

    # Tickets
    path('ticket/create/', views.create_ticket_view, name='create_ticket'),
    path(
        'ticket/<int:ticket_id>/edit/',
        views.edit_ticket_view,
        name='edit_ticket'
    ),
    path(
        'ticket/<int:ticket_id>/delete/',
        views.delete_ticket_view,
        name='delete_ticket'
    ),

    # Reviews
    path(
        'review/create/',
        views.create_ticket_review_view,
        name='create_ticket_review'
    ),
    path(
        'review/create/<int:ticket_id>/',
        views.create_review_view,
        name='create_review'
    ),
    path(
        'review/<int:review_id>/edit/',
        views.edit_review_view,
        name='edit_review'
    ),
    path(
        'review/<int:review_id>/delete/',
        views.delete_review_view,
        name='delete_review'
    ),

    # Posts et abonnements
    path('posts/', views.posts_view, name='posts'),
    path('subscriptions/', views.subscriptions_view, name='subscriptions'),
    path(
        'unfollow/<int:user_id>/',
        views.unfollow_user_view,
        name='unfollow_user'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
