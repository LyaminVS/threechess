from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from main.models import Game
from .logic import game

_COLOR_RU = {
    "white": "белые",
    "black": "чёрные",
    "red": "красные",
    "random": "случайный",
}


def _game_page_context(game_obj, user, spectator=False):
    """Данные для правой панели на странице партии (и для window.__BOARD_INIT__)."""
    room_id = str(game_obj.id)
    if spectator:
        return {
            "panel_room_id": room_id,
            "panel_color_text": "белые (обзор)",
            "panel_mode_text": "Наблюдатель",
            "panel_is_sandbox": game_obj.is_sandbox,
            "panel_sandbox_ordered_turn": game_obj.sandbox_ordered_turn,
        }
    if game_obj.is_sandbox:
        color_text = "Все цвета (песочница)"
    elif user == game_obj.player_1:
        color_text = _COLOR_RU.get(game_obj.color_1, game_obj.color_1 or "—")
    elif user == game_obj.player_2:
        color_text = _COLOR_RU.get(game_obj.color_2, game_obj.color_2 or "—")
    elif user == game_obj.player_3:
        color_text = _COLOR_RU.get(game_obj.color_3, game_obj.color_3 or "—")
    else:
        color_text = "—"
    return {
        "panel_room_id": room_id,
        "panel_color_text": color_text,
        "panel_mode_text": "Игрок",
        "panel_is_sandbox": game_obj.is_sandbox,
        "panel_sandbox_ordered_turn": game_obj.sandbox_ordered_turn,
    }


@csrf_exempt
def join_game(request, room_code):
    if request.method == 'GET' and request.user.is_authenticated:
        user = request.user
        is_spectator = request.GET.get("is_spectator") == "1"
        if not Game.objects.filter(id=room_code).exists():
            return redirect("/lobby/")
        game_obj = Game.objects.get(id=room_code)
        if is_spectator:
            ctx = _game_page_context(game_obj, user, spectator=True)
            return render(request, "main/main.html", ctx)
        success = False
        if any(is_player_arr := [getattr(game_obj, f"player_{i}") == user for i in range(1, 4)]):
            setattr(game_obj, f"disconnected_{is_player_arr.index(True) + 1}", "reconnected")
            game_obj.save()
            ctx = _game_page_context(game_obj, user, spectator=False)
            return render(request, "main/main.html", ctx)
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
        if success:
            game_obj.save()
            ctx = _game_page_context(game_obj, user, spectator=False)
            return render(request, "main/main.html", ctx)
        return redirect("/lobby/")
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
                "sandbox": game_obj.is_sandbox,
                "sandbox_ordered_turn": game_obj.sandbox_ordered_turn,
            })
        def _player_payload(ready, color):
            return {
                "success": True,
                "color": color,
                "ready": ready,
                "is_started": game_obj.status == "started",
                "sandbox": game_obj.is_sandbox,
                "sandbox_ordered_turn": game_obj.sandbox_ordered_turn,
            }

        if request.user == game_obj.player_1:
            return JsonResponse(_player_payload(game_obj.ready_1, game_obj.color_1))
        if request.user == game_obj.player_2:
            return JsonResponse(_player_payload(game_obj.ready_2, game_obj.color_2))
        if request.user == game_obj.player_3:
            return JsonResponse(_player_payload(game_obj.ready_3, game_obj.color_3))

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
            "sandbox": game_obj.is_sandbox,
            "sandbox_ordered_turn": game_obj.sandbox_ordered_turn,
        })
    return JsonResponse({
        "success": False
    })
