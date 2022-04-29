from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .logic import game


def index(request):
    return render(request, 'main/main.html')


@csrf_exempt
def change_position(request):
    data = request.POST
    cell = data['cell']
    old_cell, figure, color = game.change_position(cell)
    return JsonResponse({"old_cell": old_cell, "cell": cell, "type": figure, "color": color})


@csrf_exempt
def get_dots(request):
    data = request.POST
    letter = data["letter"]
    number = data["number"]
    dots = game.get_dots(letter + number)
    return JsonResponse({"dots": dots})


@csrf_exempt
def get_board(request):
    return JsonResponse({"figures": game.__transform_to_array__()})


@csrf_exempt
def reset(request):
    game.reset()
    return JsonResponse({})
