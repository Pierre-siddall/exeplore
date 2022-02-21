from django.db import models

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key = True)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    email = models.EmailField(max_length  = 100)
    password = models.CharField(max_length = 100) 

class Player(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    badges = models.ForeignKey(Badges, on_delete = models.CASCADE)
    visits = models.ForeignKey(Visits, on_delete = models.CASCADE)
    score = models.IntegerField()