from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import PasswordChangeFormRu, ProfileForm


@login_required
def profile(request, user_id):
    if request.user.pk != int(user_id):
        return redirect("profile", user_id=request.user.pk)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные профиля сохранены.")
            return redirect("profile", user_id=request.user.pk)
    else:
        form = ProfileForm(instance=request.user)

    return render(
        request,
        "userpage/userpage.html",
        {"form": form},
    )


@login_required
def password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeFormRu(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль успешно изменён.")
            return redirect("profile", user_id=request.user.pk)
    else:
        form = PasswordChangeFormRu(request.user)

    return render(
        request,
        "userpage/password_change.html",
        {"form": form},
    )


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("/lobby/")
