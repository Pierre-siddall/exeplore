"""This file represents all the models needed for visits - Location and Badge"""
from django.db import models

class Location(models.Model):
    """This class represents a Location, with accuracy enough for Google Maps API
    It also allows uploading an image to be used as an icon"""
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    #both of these are required for a location and can't be null
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    location_name = models.CharField(max_length=200)
    point_value = models.IntegerField()
    icon= models.FileField(upload_to='images/', null=True, verbose_name="icon for location")

    def __str__(self):
        return self.location_name

    def get_lat(self):  
        return self.latitude

    def get_long(self):
        return self.longitude

class Badge(models.Model):
    """This class represents a Badge, with the four classifications, as well
    as a FileField used for uploading an icon"""
    PLATINUM = 'PT'
    GOLD = 'AU'
    SILVER = 'AG'
    BRONZE = 'BR'
    TIERS = [
        (PLATINUM, 'Platinum'),
        (GOLD, 'Gold'),
        (SILVER, 'Silver'),
        (BRONZE, 'Bronze') ]
    badge_name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    tier = models.CharField(max_length=2, choices=TIERS, default=BRONZE,)
    icon = models.FileField(upload_to='images/', null=True, verbose_name="icon for badge")
    def __str__(self):
        return self.badge_name
