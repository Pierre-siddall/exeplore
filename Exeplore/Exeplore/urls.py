"""Exeplore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name="main"

urlpatterns = [
    path('splash/', views.splash, name="splash"),
    path('home/', views.home,name="home"),
    path('register/', views.register, name = 'register'),
    path('login/', views.login_view, name ='login'),
    path('admin/', admin.site.urls),
    path('visits/', include('visits.urls')),
    path('settings/', views.settings,name="settings"),
    path('locations/', views.locations,name="locations"),
    path('badges/', views.badges,name="badges"),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

