"""This is the file to hold the models for everything relating to users
 - namely Player, Visits, and Earned Badges for a specific User"""
from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from visits.models import Badge, Location
User = get_user_model()


class Player(models.Model):
    """This class represents the Player model within the app"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Player")
    badges = models.ManyToManyField(
        Badge, verbose_name="Badges", through='EarnedBadge')
    visits = models.ManyToManyField(
        Location, verbose_name="Visits", through='Visit')
    score = models.IntegerField("Score", default=0)
    streak = models.IntegerField("Streak", default=0)

    def set_score(self, location):
        """This function sets the score given a location's point value"""
        self.score += location.point_value

    def get_level(self):
        """This function gives the level of the player"""
        return int(self.score/10)

    def extend_streak(self):
        """This function extends the player's streak"""
        self.streak += 1

    def reset_streak(self):
        """This functions resets the player's streak"""
        self.streak = 0

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """This is called when it receives the signal from the User that a new User has
    been created"""
    if created:
        Player.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """This is called to save the player when it receives the signal from a User
    that a User has been saved"""
    instance.player.save()


class Visit(models.Model):
    """This class represents a Player's visit to a Location, with a time stamp.
    It is the middle man table for the ManyToMany relationship between Player and Location."""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    visit_datetime = models.DateTimeField("Date and time visited",
                                          auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.location.location_name


class EarnedBadge(models.Model):
    """This class represents a Player's earning of a Badge, with a timestamp.
    It's the middle man table for the ManyToMany relationship between Player and Badge"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    badge_earned_datetime = models.DateTimeField("Date and time earned",
                                                 auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.badge.badge_name
