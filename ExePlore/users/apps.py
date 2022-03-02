"""This file holds the app configuration to link to the django installed apps setting"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """This is the configuration for the User"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
