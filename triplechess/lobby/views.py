import json

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
    res = []
    game_list = list(Game.objects.filter(status="in_lobby"))

    for game in game_list:
        p_1 = game.player_1.username if game.player_1 else game.player_1
        p_2 = game.player_2.username if game.player_2 else game.player_2
        p_3 = game.player_3.username if game.player_3 else game.player_3
        res.append({
            "player_1": p_1,
            "player_2": p_2,
            "player_3": p_3,
            "board": game.board,
            "id": game.id
        })
    res = json.dumps(res)
    return JsonResponse({"games": res})


@csrf_exempt
def new_game(request):
    if request.method == 'POST':
        user = request.user
        game = Game.create(user, None, None, "boardtest")
        game.save()
    return JsonResponse({})

@csrf_exempt
def join_game(request, room_id):
    if request.method == 'GET':
        user = request.user
        game = Game.objects.get(id=room_id)
        success = False
        if not game.player_1:
            success = True
            game.player_1 = user
        elif not game.player_2:
            success = True
            game.player_2 = user
        elif not game.player_3:
            success = True
            game.player_3 = user
        game.save()

        if success:
            return redirect("/room/" + room_id + "/")
        else:
            return redirect("/lobby/")

def join_room(request, room_id):
    return render(request, 'lobby/room.html')