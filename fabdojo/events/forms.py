from django import forms
from dal import autocomplete

from .models import *
from card.models import *

class CardForm(forms.ModelForm):

    class Meta:
        model = CardInfo
        fields = ('card', 'card_count')
        widgets = {
            'card' : autocomplete.ModelSelect2(url='events:card-autocomplete',
                                               )
        }
