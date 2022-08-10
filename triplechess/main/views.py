from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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
        data = request.POST.dict()
        game_obj = Game.objects.get(id=room_code)
        if (request.user == game_obj.player_1 and game_obj.color_1 == data["color"]) or \
                (request.user == game_obj.player_2 and game_obj.color_2 == data["color"]) or \
                (request.user == game_obj.player_3 and game_obj.color_3 == data["color"]):
            return JsonResponse({
                "success": True,
            })
    return JsonResponse({
        "success": False,
    })


@csrf_exempt
def get_color(request, room_code):
    if request.user.is_authenticated:
        game_obj = Game.objects.get(id=room_code)
        if request.user == game_obj.player_1:
            return JsonResponse({
                "success": True,
                "color": game_obj.color_1,
            })
        if request.user == game_obj.player_2:
            return JsonResponse({
                "success": True,
                "color": game_obj.color_2,
            })
        if request.user == game_obj.player_3:
            return JsonResponse({
                "success": True,
                "color": game_obj.color_3,
            })

    return JsonResponse({
        "success": False,
    })
