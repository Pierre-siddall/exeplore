from django.db import models

# Create your models here.
<<<<<<< HEAD
=======
class User(models.Model):
    id = models.IntegerField("user ID number", primary_key = True)
    first_name = models.CharField("user's first name", max_length = 100)
    last_name = models.CharField("user's last name", max_length = 100)
    username = models.CharField("user's username", max_length = 100)
    email = models.EmailField("user's email, must end in @exeter.ac.uk",max_length  = 100)
    password = models.CharField("user's password", max_length = 100)

class Player(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, verbose_name = "the user account that this player is")
    badges = models.ForeignKey(Badges, on_delete = models.CASCADE, verbose_name = "list of badges this user has earned")
    visits = models.ForeignKey(Visits, on_delete = models.CASCADE, verbose_name = "list of visits for this user")
    score = models.IntegerField("total score for this user")
>>>>>>> parent of 16e8881 (Merge pull request #8 from jennischofield/main)
