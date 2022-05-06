from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
# Create your views here.

def index(request):
    return render(request, 'lobby/main.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'lobby/main.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'lobby/register.html', {'user_form': user_form})

def login(request):
    pass


def on_open(request):
    if request.user.is_authenticated:
        return redirect("login/")
    if not request.user.is_authenticated:
        return redirect("register/")