from django.db import models

# Create your models here.

class CardType(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class Card(models.Model):
    card_id=models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    set = models.CharField(max_length=100, blank=True, null=True)
    pitch = models.IntegerField(default=0)
    cost = models.CharField(max_length=2, blank=True, null=True)
    power = models.CharField(max_length=2, blank=True, null=True)
    defense = models.CharField(max_length=2, blank=True, null=True)
    card_class = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=50)
    sub_type = models.CharField(max_length=50)
    rarity = models.CharField(max_length=20)
    text = models.TextField()


    def __str__(self):
        if self.pitch == 1:
            colour = 'RED'
        elif self.pitch == 2:
            colour = 'YELLOW'
        elif self.pitch == 3:
            colour = 'BLUE'
        else:
            colour = ""
        return "%s %s" % (self.name, colour)

class Hero(models.Model):
    name = models.CharField(max_length=50)
    young_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
