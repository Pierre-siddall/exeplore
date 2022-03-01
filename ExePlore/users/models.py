from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from visits.models import Badge, Location
from django.db.models.signals import post_save
from django.dispatch import receiver
User = get_user_model()

class Player(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, verbose_name = "Player")
    badges = models.ManyToManyField(Badge, verbose_name = "Badges",through='Earned_Badge')
    visits = models.ManyToManyField(Location, verbose_name = "Visits", through='Visit')
    score = models.IntegerField("Score", default= 0)
    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.player.save()

class Visit(models.Model):
    player = models.ForeignKey(Player, on_delete= models.CASCADE)
    location = models.ForeignKey(Location, on_delete = models.CASCADE)
    visit_datetime = models.DateTimeField("Date and time visited", auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.location.location_name
    
class Earned_Badge(models.Model):
    player = models.ForeignKey(Player, on_delete= models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete = models.CASCADE)
    badge_earned_datetime = models.DateTimeField("Date and time earned", auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.badge.badge_name
    
    

