"""fabdojo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from util.views import card_upload, deck_upload

urlpatterns = [
    path('', include('events.urls')),
    path('upload-cards/', card_upload, name="card_upload"),
    path('upload-deck/', deck_upload, name="deck_upload"),
    path('cheeseburger/', admin.site.urls),
]
