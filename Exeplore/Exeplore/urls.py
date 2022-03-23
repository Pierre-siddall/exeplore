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
from django.conf import settings
from django.conf.urls.static import static
from . import views


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
    path('', views.splash, name="splash"),
    path('logout/', views.logout_view, name ='logout'),
    path('add_location/', views.add_location, name = 'add_location'),
    path('del_location/', views.del_location, name = 'del_location'),
    path('add_badge/', views.add_badge, name = 'add_badge'),
    path('del_badge/', views.del_badge, name = 'del_badge'),
    path('add_user/', views.add_user, name = 'add_user'),
    path('del_user/', views.del_user, name = 'del_user'),
    path('edit_user/', views.edit_user, name = 'edit_user'),
    path('scanning/', views.scanning, name = 'scanning'),
    path('leaderboard/', views.leaderboard, name ='leaderboard')
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
