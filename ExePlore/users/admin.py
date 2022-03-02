"""This file is made to set up the administration of the website, including
the formatting of Players and Users"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from users.models import Player, Visit, EarnedBadge

User = get_user_model()

class PlayerInLine(admin.StackedInline):
    """Defines the inline admin descriptor for Player"""
    model = Player
    can_delete = False
    verbose_name_plural = 'players'

class UserAdmin(BaseUserAdmin):
    """Defines the User admin"""
    inlines = (PlayerInLine,)

class VisitInLine(admin.StackedInline):
    """Defines the inline admin descriptor for Visit"""
    model = Visit
    can_delete = True
    readonly_fields = ('visit_datetime', )
    verbose_name = "Visit"
    verbose_name_plural = "visits"

class EarnedBadgeInLine(admin.StackedInline):
    """Defines the inline admin descriptor for Earned Badges"""
    model = EarnedBadge
    readonly_fields = ('badge_earned_datetime', )
    list_display = ['badge',]
    can_delete = True
    verbose_name = "Badge"
    verbose_name_plural = "earned badges"

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Defines the admin for the Player class"""
    model = Player
    list_display = ['name',]
    def name(self, obj):
        """Returns the name of the object"""
        return obj.user.username
    def get_visits(self,instance):
        """Returns all the Player's visits"""
        return [visit.name for visit in instance.visits.all()]
    def get_badges(self,instance):
        """Returns all the Player's badges"""
        return [badge.name for badge in instance.badges.all()]
    inlines = [VisitInLine, EarnedBadgeInLine]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Player)
admin.site.register(Player, PlayerAdmin)
