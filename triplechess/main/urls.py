from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.index),
    path('board/change_position/', views.change_position),
    path("board/get_dots/", views.get_dots),
    path("board/get_board/", views.get_board),
    path("board/reset/", views.reset),
    path("board/reset_dots/", views.reset_dots),
    path('board/<room_code>/', views.index),
]
