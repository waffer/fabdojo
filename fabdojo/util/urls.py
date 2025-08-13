from django.urls import path

from .views import *

app_name = 'util'
#url to point to cc/blitz filtered event
#contact us page
#event view page
#event list page
#decklist page

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]