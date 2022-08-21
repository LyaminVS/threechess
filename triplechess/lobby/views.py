import json
import random

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login
from main.models import Game
from main.logic.game import Game as GameClass


# Create your views here.

def index(request):
    return render(request, 'lobby/lobby.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
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
                return render(request, 'lobby/login.html',
                              {'form': form, 'borders_login': "red", 'borders_password': "red"})
        else:
            return render(request, 'lobby/login.html',
                          {'form': form, 'borders_login': "red", 'borders_password': "red"})
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
    filter_status = request.POST.get("filter_status")
    game_list = list(Game.objects.filter(status=filter_status))
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
    if request.method == 'GET' and request.user.is_authenticated:
        new_g = GameClass().game_to_json()
        game = Game.create(None, None, None, new_g)
        colors = ["white", "black", "red"]
        random.shuffle(colors)
        game.color_1 = colors[0]
        game.color_2 = colors[1]
        game.color_3 = colors[2]
        game.save()
        return JsonResponse({
            "success": True,
            "room_id": str(game.id),
        })
    return JsonResponse({
        "success": False,
    })
