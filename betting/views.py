from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import View
from .models import Bet, Game
from .forms import UserForm

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
    fields = ['game', 'type', 'wager', 'betvalue', 'userId', 'odds', 'betpick']

class UserFormView(View):
    form_class = UserForm
    template_name = 'betting/registration_form.html'    

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('betting:index')

        return render(request, self.template_name, {'form':form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                games = Game.objects.all()
                return render(request, 'betting/index.html', {'all_games': games})
            else:
                return render(request, 'betting/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'betting/login.html', {'error_message': 'Invalid login'})
    return render(request, 'betting/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'betting/login.html', context)





















