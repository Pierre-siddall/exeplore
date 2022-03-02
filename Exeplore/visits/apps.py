"""This file defines the config for Visits for Django's installed apps"""
from django.apps import AppConfig


class VisitsConfig(AppConfig):
    """This class defines the Visit's app config"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visits'
