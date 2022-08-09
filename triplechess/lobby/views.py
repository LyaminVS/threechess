import json

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
    if request.method == 'GET' and request.user.is_authenticated:
        user = request.user
        new_g = GameClass().game_to_json()
        game = Game.create(user, None, None, new_g)
        game.save()
        return JsonResponse({
            "success": True,
            "room_id": str(game.id),
        })
    return JsonResponse({
        "success": False,
    })


@csrf_exempt
def join_game(request, room_id):
    if request.method == 'GET' and request.user.is_authenticated:
        user = request.user
        game = Game.objects.get(id=room_id)
        success = False
        if not (game.player_1 == user or game.player_2 == user or game.player_3 == user):
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
        else:
            return redirect("../../../board/" + room_id + "/")
        if success:
            return redirect("../../../board/" + room_id + "/")
        else:
            return redirect("/lobby/")
    else:
        return redirect("/login/")


# def join_room(request, room_id):
#     if request.method == 'GET' and request.user.is_authenticated:
#         user = request.user
#         res = {}
#         game = Game.objects.get(id=room_id)
#         if game.player_1 == user or game.player_2 == user or game.player_3 == user:
#             res["player_1_name"] = game.player_1.username if game.player_1 else None
#             res["player_2_name"] = game.player_2.username if game.player_2 else None
#             res["player_3_name"] = game.player_3.username if game.player_3 else None
#             if game.player_1 == user:
#                 res["player_num"] = 1
#             if game.player_2 == user:
#                 res["player_num"] = 2
#             if game.player_3 == user:
#                 res["player_num"] = 3
#             return render(request, 'lobby/room.html', res)
#     return redirect("../../login/")
#
#
# @csrf_exempt
# def button_pressed_check(request, room_id):
#     if request.method == 'POST' and request.user.is_authenticated:
#         user = request.user
#         game = Game.objects.get(id=room_id)
#         data = request.POST.dict()
#         if int(data["player"]) == 1 and game.player_1 == user:
#             if game.ready_1 == 0:
#                 game.ready_1 = 1
#                 game.color_1 = data["radio"]
#             else:
#                 game.ready_1 = 0
#         if int(data["player"]) == 2 and game.player_2 == user:
#             if game.ready_2 == 0:
#                 game.ready_2 = 1
#                 game.color_2 = data["radio"]
#             else:
#                 game.ready_2 = 0
#         if int(data["player"]) == 3 and game.player_3 == user:
#             if game.ready_3 == 0:
#                 game.ready_3 = 1
#                 game.color_3 = data["radio"]
#             else:
#                 game.ready_3 = 0
#         game.save()
#         return JsonResponse({})
