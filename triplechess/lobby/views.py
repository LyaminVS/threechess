import json
import random

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

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
            return render(request, 'lobby/register.html', {'new_user': new_user})
        return render(request, 'lobby/register.html', {'user_form': user_form})
    user_form = UserRegistrationForm()
    return render(request, 'lobby/register.html', {'user_form': user_form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/lobby/")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None and user.is_active:
                login(request, user)
                return redirect("/lobby/")
            return render(
                request,
                'lobby/login.html',
                {'form': form, 'login_error': True},
            )
        return render(request, 'lobby/login.html', {'form': form})
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
    statuses = [filter_status]
    if filter_status == "in_lobby":
        statuses.append("setup")
    game_list = Game.objects.filter(status__in=statuses, is_sandbox=False)
    if request.user.is_authenticated:
        game_list = game_list.filter(Q(is_private=False) | Q(owner=request.user))
    else:
        game_list = game_list.filter(is_private=False)
    game_list = list(game_list)
    for game in game_list:
        p_1 = game.player_1.username if game.player_1 else game.player_1
        p_2 = game.player_2.username if game.player_2 else game.player_2
        p_3 = game.player_3.username if game.player_3 else game.player_3
        res.append({
            "player_1": p_1,
            "player_2": p_2,
            "player_3": p_3,
            "board": game.board,
            "id": game.id,
            "is_sandbox": game.is_sandbox,
            "is_private": game.is_private,
            "can_delete": request.user.is_authenticated and request.user.is_superuser,
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


@csrf_exempt
@require_GET
def new_sandbox_game(request):
    """
    Тестовая партия для суперпользователя: сразу started, один игрок на все три цвета,
    без очереди хода (логика в consumer).
    """
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({"success": False, "error": "forbidden"}, status=403)
    new_g = GameClass().game_to_json()
    u = request.user
    game = Game.create(u, u, u, new_g)
    game.owner = u
    game.color_1 = "white"
    game.color_2 = "black"
    game.color_3 = "red"
    game.is_sandbox = True
    game.sandbox_ordered_turn = False
    game.status = "started"
    game.ready_1 = game.ready_2 = game.ready_3 = 1
    game.save()
    return JsonResponse({
        "success": True,
        "room_id": str(game.id),
        "sandbox": True,
    })


@csrf_exempt
@require_GET
def new_private_game(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "forbidden"}, status=403)
    g = GameClass()
    g.clear_board_for_setup()
    new_g = g.game_to_json()
    u = request.user
    game = Game.create(u, u, u, new_g)
    game.owner = u
    game.color_1 = "white"
    game.color_2 = "black"
    game.color_3 = "red"
    game.is_sandbox = True
    game.is_private = True
    game.sandbox_ordered_turn = True
    game.status = "setup"
    game.ready_1 = game.ready_2 = game.ready_3 = 0
    game.save()
    return JsonResponse({
        "success": True,
        "room_id": str(game.id),
        "sandbox": True,
        "private": True,
    })


@csrf_exempt
def delete_game(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "method_not_allowed"}, status=405)
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({"success": False, "error": "forbidden"}, status=403)
    game_id = request.POST.get("game_id")
    if not game_id:
        return JsonResponse({"success": False, "error": "game_id_required"}, status=400)
    if not Game.objects.filter(id=game_id).exists():
        return JsonResponse({"success": False, "error": "not_found"}, status=404)
    Game.objects.get(id=game_id).delete()
    return JsonResponse({"success": True})
