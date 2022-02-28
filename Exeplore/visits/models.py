from django.db import models

class Location(models.Model):
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    #both of these are required for a location and can't be null
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    location_name = models.CharField(max_length=200)
    point_value = models.IntegerField()
    
    def __str__(self):
        return self.location_name
class Badge(models.Model):
    badge_name = models.CharField(max_length = 200)
    description = models.CharField(max_length=300)
    #not quite sure how to implement requirements, prob something on the front end/middle
    
