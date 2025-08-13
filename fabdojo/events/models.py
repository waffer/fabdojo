from card.models import *
from django.db import models
from django_countries.fields import CountryField

# Create your models here.

class Format(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class TournamentType(models.Model):
    name = models.CharField(max_length=200)
    level = models.IntegerField(default=4)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    country = CountryField(default='NZ')
    event_date = models.DateTimeField('event date')
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, blank=True, null=True, related_name='event')
    format = models.ForeignKey(Format, blank=True, null=True, on_delete=models.PROTECT, related_name='event')
    tournament_type = models.ForeignKey(TournamentType, blank=True, null=True, on_delete=models.PROTECT, related_name='event')
    def __str__(self):
        return self.name

    def get_date(self):
        return self.event_date.strftime("%d %b %Y")

class Player(models.Model):
    name = models.CharField(max_length=200)
    country = CountryField()
    gem_id = models.IntegerField(primary_key=True)
    def __str__(self):
        return self.name

class Decklist(models.Model):
    deck_id = models.AutoField(primary_key=True)
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='deck')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True, related_name='deck')
    deck_name = models.CharField(max_length=200, blank=True, null=True)
    hero = models.ForeignKey(Hero, on_delete=models.SET_NULL, blank=True, null=True, related_name='deck')
    cards = models.ManyToManyField(Card, through='CardInfo')
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.deck_name

    def get_card_count(self):
        total = 0
        for card in self.cardInfo.all():
            total += card.card_count
        return total

    def save(self, *args, **kwargs):
        self.deck_name = "{0}-{1} - {2}".format(self.player_id, self.hero, self.event)
        super(Decklist, self).save(*args, **kwargs)

    def get_placings(self):
        if self.position == 3 or self.position == 4:
            position = "3-4th"
        elif self.position == 5 or self.position == 6 or self.position == 7 or self.position == 8:
            position = "5-8th"
        elif self.position == 1:
            position = "1st"
        elif self.position == 2:
            position = "2nd"
        else:
            position = self.position
        return position

    def get_hero_name(self):
        if self.event.format.code == "CC":
            return self.hero.name;
        else:
            return self.hero.young_name;

class CardInfo(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='cardInfo')
    deck = models.ForeignKey(Decklist, on_delete=models.CASCADE, related_name='cardInfo')
    card_count = models.IntegerField(default=1)

    def __str__(self):
        return self.card.name
