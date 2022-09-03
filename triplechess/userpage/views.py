from django.shortcuts import render
from django.http import JsonResponse

def userpage(request, user_id):
    print(1312313)
    return JsonResponse({
        "success": True
    })