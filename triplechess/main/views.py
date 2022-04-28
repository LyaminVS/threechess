from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logic.board as logic

board = logic.Board()

def index(request):
    return render(request, 'main/main.html')


@csrf_exempt
def change_position(request):
    data = request.POST
    print(data['hello'])
    return JsonResponse({"code": 10000, "content": ""})


@csrf_exempt
def get_dots(request):
    data = request.POST
    letter = data["letter"]
    number = data["number"]
    dots = logic.board.board.get_dots(letter + number)
    print(dots)


