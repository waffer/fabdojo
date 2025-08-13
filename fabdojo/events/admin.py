from django.contrib import admin
from django import forms
from .forms import *

from .models import *
# Register your models here.

class CardInline(admin.TabularInline):
    model = CardInfo
    form = CardForm
    extra = 39

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "card":
            kwargs["queryset"] = Card.objects.all().order_by('name')
        return super(CardInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)

        formfield.widget.can_delete_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_add_related = False  # can change this, too
        formfield.widget.can_view_related = False  # can change this, too

        return formfield

class DecklistInline(admin.TabularInline):
    model = Decklist
    show_change_link = True
    readonly_fields = ('player_id', 'deck_name', 'hero', 'position')

class DecklistAdmin(admin.ModelAdmin):
    inlines = [CardInline]
    list_display = ('player_id', 'event', 'get_event_date', 'get_card_count')
    exclude = ('deck_id','deck_name')

    readonly_fields = ('get_card_count',)

    list_filter = ['event__format', 'event__store']

    def get_event_date(self, obj):
        return obj.event.event_date

    def get_event_format(self, obj):
        return obj.event.format

class EventAdmin(admin.ModelAdmin):
    inlines = [DecklistInline]
    list_display = ('name', 'format', 'store', 'event_date')
    search_fields = ['store']
    list_filter = ['format', 'store', 'tournament_type']

class PlayerAdmin(admin.ModelAdmin):
    model = Player
    list_display = ("name", "country", "gem_id",)
    search_fields = ['name']

class StoreAdmin(admin.ModelAdmin):
    model = Store
    list_display = ("name",)
    search_fields = ['name']


admin.site.register(Decklist, DecklistAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Format)
admin.site.register(Store, StoreAdmin)
admin.site.register(TournamentType)