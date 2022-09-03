from django.urls import path
from . import views

urlpatterns = [
    path("user/<user_id>/", views.userpage)
]
