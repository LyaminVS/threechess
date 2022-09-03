from django.shortcuts import render, redirect
from django.http import JsonResponse

def userpage(request, user_id):
    if request.user.is_authenticated:
        return render(request, "userpage/userpage.html")
    else:
        return redirect("../lobby")