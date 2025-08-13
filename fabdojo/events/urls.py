from django.urls import path
from django.conf.urls import url
from dal import autocomplete

from .views import *
from card.models import *

app_name = 'events'
#url to point to cc/blitz filtered event
#contact us page
#event view page
#event list page
#decklist page

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('event_list/<str:format>',EventListView.as_view(), name='event_list'),
    path('event/<int:pk>', EventView.as_view(), name='event'),
    path('deck/<int:pk>', DecklistView.as_view(), name='decklist'),
    path('player/<int:pk>', PlayerView.as_view(), name='player'),
    path('hero/<str:hero>', HeroView.as_view(), name='hero'),
    path('compare/<str:hero>/<str:format>', DeckCompareView.as_view(), name='compare'),
    url( 'card-autocomplete/$',autocomplete.Select2QuerySetView.as_view(model=Card),name='card-autocomplete',),
]