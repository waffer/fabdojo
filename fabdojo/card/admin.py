from django.contrib import admin

from .models import *

# Register your models here.

class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'pitch', 'type', 'sub_type', 'card_id')
    search_fields = ['name']

    list_filter = ['set', 'card_class', 'type']


admin.site.register(Hero)
admin.site.register(Card, CardAdmin)
