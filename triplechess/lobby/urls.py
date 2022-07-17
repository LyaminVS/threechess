from django.urls import path
from . import views

urlpatterns = [
    path('lobby/', views.index),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('lobby/get_list/', views.get_list),
    path('lobby/new_game/', views.new_game),
    path('', views.on_open),
    path('lobby/room/<room_id>/', views.join_game),
    path('room/<room_id>/', views.join_room)
]
