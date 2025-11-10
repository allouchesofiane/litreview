from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Ticket, Review, UserFollows


# ==================== ADMIN UTILISATEUR PERSONNALISÉ ====================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuration de l'admin pour le modèle User personnalisé"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    # Ces champs sont nécessaires pour UserAdmin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


# ==================== ADMIN TICKET ====================

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Configuration de l'administration des Tickets"""
    list_display = ('title', 'user', 'time_created', 'has_image')
    list_filter = ('time_created', 'user')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'time_created'
    readonly_fields = ('time_created',)

    def has_image(self, obj):
        """Affiche si le ticket a une image"""
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Image"


# ==================== ADMIN REVIEW ====================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Configuration de l'administration des Reviews"""
    list_display = ('headline', 'user', 'ticket', 'rating', 'time_created')
    list_filter = ('rating', 'time_created', 'user')
    search_fields = ('headline', 'body', 'user__username', 'ticket__title')
    date_hierarchy = 'time_created'
    readonly_fields = ('time_created',)


# ==================== ADMIN USERFOLLOWS ====================

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """Configuration de l'administration des abonnements"""
    list_display = ('user', 'followed_user', 'id')
    list_filter = ('user', 'followed_user')
    search_fields = ('user__username', 'followed_user__username')

    def has_add_permission(self, request):
        """Permet l'ajout depuis l'admin"""
        return True

    def has_change_permission(self, request, obj=None):
        """Empêche la modification depuis l'admin"""
        return False