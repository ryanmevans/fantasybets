from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bet, Game

class IndexView(generic.ListView):
    template_name = 'betting/index.html'
    context_object_name = 'all_games'    

    def get_queryset(self):
        return Game.objects.all()

class DetailView(generic.DetailView):
    model = Game
    template_name = 'betting/detail.html'

class BetsView(generic.ListView):
    template_name = 'betting/mybets.html';
    context_object_name = 'all_bets'

    def get_queryset(self):
        return Bet.objects.all()

class BetCreate(CreateView):
    model = Bet
    fields = ['game', 'type', 'wager', 'betvalue', 'userId', 'odds', 'hometeam', 'awayteam', 'gamedate', 'betpick']

            
