from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()

from users.models import Player, Visit, Earned_Badge

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class PlayerInLine(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'players'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PlayerInLine,)

class VisitInLine(admin.StackedInline):
    model = Visit
    can_delete = True
    verbose_name = "Visit"
    verbose_name_plural = "visits"
class EarnedBadgeInLine(admin.StackedInline):
    model = Earned_Badge
    readonly_fields = ('badge_earned_datetime', )
    list_display = ['badge',]
    can_delete = True
    verbose_name = "Badge"
    verbose_name_plural = "earned badges"
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    model = Player
    list_display = ['name',]
    def name(self, obj):
        return obj.user.username
    def get_visits(self,instance):
        return [visit.name for visit in instance.visits.all()]
    def get_badges(self,instance):
        return [badge.name for badge in instance.badges.all()]
    inlines = [VisitInLine, EarnedBadgeInLine]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Player)
admin.site.register(Player, PlayerAdmin)