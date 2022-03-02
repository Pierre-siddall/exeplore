"""This file holds the admin manager classes for everything to do with
visiting and locations"""
from django.contrib import admin
from users.models import Player, EarnedBadge, Visit
from visits.models import Badge, Location

# Register your models here.
class PlayerInLine(admin.StackedInline):
    """This class defines how a Player should be displayed in Django's admin"""
    model = Player
    can_delete = False
    verbose_name_plural = 'players'
    list_display = ['name']

class EarnedBadgeInLine(admin.StackedInline):
    """This class defines how a EarnedBadge should be displayed in Django's admin"""
    model = EarnedBadge
    readonly_fields = ('badge_earned_datetime', )
    list_display = ['badge',]
    can_delete = True
    verbose_name = "Player"
    verbose_name_plural = "Players"
class BadgeAdmin(admin.ModelAdmin):
    """This class defines how Badges are managed, and how their many-to-many
    relationship should be displayed in admin"""
    model = Badge
    inlines = [EarnedBadgeInLine,  ]
class VisitInLine(admin.StackedInline):
    """This class defines how a Visit should be displayed in
    
    Django's admin"""
    model = Visit
    readonly_fields = ('visit_datetime', )
    list_display = ['visit',]
    can_delete = True
    verbose_name = "Player"
    verbose_name_plural = "Players"

class LocationAdmin(admin.ModelAdmin):
    """This class defines how Locations are managed, and how their many-to-many
    relationship should be displayed in admin"""
    model = Location
    inlines = [VisitInLine, ]

admin.site.register(Badge, BadgeAdmin)
admin.site.register(Location, LocationAdmin)
