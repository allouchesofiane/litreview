from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Ticket, Review, UserFollows



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuration de l'admin pour le modèle User personnalisé"""
    list_display = ('username', 'is_staff', 'date_joined')
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


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Configuration de l'administration des Tickets"""
    list_display = ('title', 'user', 'time_created', 'has_image')
    date_hierarchy = 'time_created'
    readonly_fields = ('time_created',)

    def has_image(self, obj):
        """Affiche si le ticket a une image"""
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Image"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Configuration de l'administration des Reviews"""
    list_display = ('headline', 'user', 'ticket', 'rating', 'time_created')
    date_hierarchy = 'time_created'
    readonly_fields = ('time_created',)

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    """Configuration de l'administration des abonnements"""
    list_display = ('user', 'followed_user', 'id')
    list_filter = ('user', 'followed_user')
    search_fields = ('user__username', 'followed_user__username')

    def has_add_permission(self, request):
        """Empêche l'ajout depuis l'admin (doit se faire via l'app)"""
        return True

    def has_change_permission(self, request, obj=None):
        """Empêche la modification depuis l'admin"""
        return False