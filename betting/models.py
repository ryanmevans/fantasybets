from __future__ import unicode_literals
import datetime
import time
from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Better(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=50000.00)

    def __str__(self):
        return self.user

def create_better(sender, instance, created, **kwargs):
    if created:
        Better.objects.create(user=instance)

post_save.connect(create_better, sender=User)

class Game(models.Model):
    hometeam = models.CharField(max_length=70)
    awayteam = models.CharField(max_length=70)
    homescore = models.IntegerField()
    awayscore = models.IntegerField()
    gamedate = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('betting:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.gamedate.strftime('%Y-%m-%d %H:%M')+'-'+self.awayteam+'@'+self.hometeam

class Bet(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    wager = models.IntegerField()
    betvalue = models.IntegerField()
    userId = models.IntegerField()
    odds = models.IntegerField()
    betpick = models.CharField(max_length=70)
    paid = models.BooleanField(default=False)

    def __str__(self):
        retstr = str(self.game) + ' - Pick: '+self.betpick
        return retstr

    def get_absolute_url(self):
        return reverse('betting:detail', kwargs={'pk': self.pk})
 
    def winAmount(self):
        if self.odds>0:
            win = float(self.wager) * (float(self.odds)/100)
            win = round(win, 2)
            return win

        elif self.odds<0:
            win = float(self.wager) * (100/float(-(self.odds)))
            win = round(win, 2)
            return win

        else:
            return wager

    def betTypeString(self):
        if self.type == "overunder":
            return "over/under"
        elif self.type == "spread":
            return "spread"
        elif self.type == "straightup":
            return "winner"

    def pickToString(self):
        if self.type == "overunder":
            return "Over/Under: %d" % (self.betvalue)
        elif self.type == "spread":
            return "Spread: %d" % (self.betvalue)
        elif self.type == "straightup":
            return "This is a straight wager on the game winner"

    def oddsToString(self):
        if self.odds > 0:
            return "+%d" % (self.odds)
        else:
            return self.odds
