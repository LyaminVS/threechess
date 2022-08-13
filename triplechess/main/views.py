from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from main.models import Game
from .logic import game


def index(request, room_code):
    if request.user.is_authenticated:
        return render(request, 'main/main.html')
    else:
        return redirect("../login/")


@csrf_exempt
def check_user(request, room_code):
    if request.user.is_authenticated:
        data = request.POST
        game_obj = Game.objects.get(id=room_code)
        if (request.user == game_obj.player_1 and game_obj.color_1 == data.get("color")) or \
                (request.user == game_obj.player_2 and game_obj.color_2 == data.get("color")) or \
                (request.user == game_obj.player_3 and game_obj.color_3 == data.get("color")):
            if game_obj.status == "started" or (not int(data.get("check_game_start"))):
                return JsonResponse({
                    "success": True,
                })
    return JsonResponse({
        "success": False,
    })


@csrf_exempt
def get_color_and_ready(request, room_code):
    if request.user.is_authenticated:
        game_obj = Game.objects.get(id=room_code)
        if request.user == game_obj.player_1:
            return JsonResponse({
                "success": True,
                "color": game_obj.color_1,
                "ready": game_obj.ready_1,
                "is_started": True,
            })
        if request.user == game_obj.player_2:
            return JsonResponse({
                "success": True,
                "color": game_obj.color_2,
                "ready": game_obj.ready_2,
                "is_started": True,
            })
        if request.user == game_obj.player_3:
            return JsonResponse({
                "success": True,
                "color": game_obj.color_3,
                "ready": game_obj.ready_3,
                "is_started": True,
            })

    return JsonResponse({
        "success": False,
    })


@csrf_exempt
def toggle_ready(request, room_code):
    game_obj = Game.objects.get(id=room_code)
    if game_obj.status != "in_lobby":
        return JsonResponse({
            "success": True,
            "ready": 1,
            "is_started": True,
        })
    if request.user == game_obj.player_1:
        game_obj.ready_1 = (game_obj.ready_1 + 1) % 2
        is_started = check_start(game_obj)
        game_obj.save()
        return JsonResponse({
            "is_started": is_started,
            "ready": game_obj.ready_1,
            "success": True,
        })
    if request.user == game_obj.player_2:
        game_obj.ready_2 = (game_obj.ready_2 + 1) % 2
        is_started = check_start(game_obj)
        game_obj.save()
        return JsonResponse({
            "is_started": is_started,
            "ready": game_obj.ready_2,
            "success": True,
        })
    if request.user == game_obj.player_3:
        game_obj.ready_3 = (game_obj.ready_3 + 1) % 2
        is_started = check_start(game_obj)
        game_obj.save()
        return JsonResponse({
            "is_started": is_started,
            "ready": game_obj.ready_3,
            "success": True,
        })
    return JsonResponse({
        "success": False,
    })


def check_start(game_obj):
    if all((game_obj.ready_1, game_obj.ready_2, game_obj.ready_3)):
        game_obj.status = "started"
        return True
    else:
        game_obj.status = "in_lobby"
        return False
