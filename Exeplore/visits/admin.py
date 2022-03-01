from django.contrib import admin
from .models import Location, Badge
from users.models import Player, Earned_Badge
from visits.models import Badge, Location
# Register your models here.
class PlayerInLine(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'players'
    list_display = ['name']
class EarnedBadgeInLine(admin.StackedInline):
    model = Earned_Badge
    readonly_fields = ('badge_earned_datetime', )
    list_display = ['badge',]
    can_delete = True
    verbose_name = "Players"
    verbose_name_plural = "Players"
class BadgeAdmin(admin.ModelAdmin):
    model = Badge 
    inlines = [EarnedBadgeInLine, ]

admin.site.register(Location)
admin.site.register(Badge, BadgeAdmin)