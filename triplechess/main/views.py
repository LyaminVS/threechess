from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def index(request):
    return render(request, 'main/main.html')


@csrf_exempt
def test(request):
    data = request.POST
    print(data['hello'])
    return JsonResponse({"code":10000, "content":""})
    # return 123
    # print(request)