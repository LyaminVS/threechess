from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login
from main.models import Game
import main.logic.game
# Create your views here.

def index(request):
    return render(request, 'lobby/lobby.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'lobby/lobby.html', {'new_user': new_user})
        else:
            errors = user_form.errors
            return render(request, 'lobby/register.html', {'errors': errors, 'user_form': UserRegistrationForm()})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'lobby/register.html', {'errors': '', 'user_form': user_form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/lobby/")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/lobby/")
            else:
                return render(request, 'lobby/login.html', {'form': form, 'borders_login': "red", 'borders_password': "red"})
        else:
            return render(request, 'lobby/login.html', {'form': form, 'borders_login': "red", 'borders_password': "red"})
    else:
        form = LoginForm()
    return render(request, 'lobby/login.html', {'form': form})


def on_open(request):
    if request.user.is_authenticated:
        return redirect("login/")
    if not request.user.is_authenticated:
        return redirect("register/")


@csrf_exempt
def get_list(request):
    return JsonResponse({})


@csrf_exempt
def new_game(request):
    if request.method == 'POST':
        user = request.user
        print(main.logic.game.Game())
        game = Game.create(user, None, None, main.logic.game.Game())
        game.save()
    return JsonResponse({})