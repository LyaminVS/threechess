from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from main.models import Game
from .logic import game


@csrf_exempt
def join_game(request, room_code):
    if request.method == 'GET' and request.user.is_authenticated:
        user = request.user
        is_spectator = request.GET.get("is_spectator")
        if is_spectator == "1":
            return render(request, 'main/main.html')
        if Game.objects.filter(id=room_code).exists():
            game_obj = Game.objects.get(id=room_code)
        else:
            return redirect("/lobby/")
        success = False
        if any(is_player_arr := [getattr(game_obj, f"player_{i}") == user for i in range(1, 4)]):
            setattr(game_obj, f"disconnected_{is_player_arr.index(True) + 1}", "reconnected")
            game_obj.save()
            return render(request, 'main/main.html')
        else:
            if not game_obj.player_1:
                success = True
                game_obj.player_1 = user
                game_obj.disconnected_1 = "connected"
            elif not game_obj.player_2:
                success = True
                game_obj.player_2 = user
                game_obj.disconnected_2 = "connected"
            elif not game_obj.player_3:
                success = True
                game_obj.player_3 = user
                game_obj.disconnected_3 = "connected"
            game_obj.save()
        if success:
            return render(request, 'main/main.html')
        else:
            return redirect("/lobby/")
    else:
        return redirect("/login/")


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
        if request.POST.get("is_spectator") == "1":
            return JsonResponse({
                "success": True,
                "is_started": True if game_obj.status == "started" else False,
            })
        if request.user == game_obj.player_1:
            return JsonResponse({
                "success": True,
                "color": game_obj.color_1,
                "ready": game_obj.ready_1,
                "is_started": True if game_obj.status == "started" else False,
            })
        if request.user == game_obj.player_2:
            return JsonResponse({
                "success": True,
                "color": game_obj.color_2,
                "ready": game_obj.ready_2,
                "is_started": True if game_obj.status == "started" else False,
            })
        if request.user == game_obj.player_3:
            return JsonResponse({
                "success": True,
                "color": game_obj.color_3,
                "ready": game_obj.ready_3,
                "is_started": True if game_obj.status == "started" else False,
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


@csrf_exempt
def first_connect(request, room_code):
    if Game.objects.filter(id=room_code).exists() and request.user.is_authenticated:
        game_obj = Game.objects.get(id=room_code)
        return JsonResponse({
            "success": True,
            "is_spectator": not any([getattr(game_obj, f"player_{i}") == request.user for i in range(1, 4)]),
        })
    return JsonResponse({
        "success": False
    })
