from django.urls import path
from . import views

urlpatterns = [
    path('board/<room_code>/', views.join_game),
    path('board/<room_code>/check_user/', views.check_user),
    path('board/<room_code>/get_color_and_ready/', views.get_color_and_ready),
    path('board/<room_code>/toggle_ready/', views.toggle_ready),
    path('board/<room_code>/first_connect/', views.first_connect)
]
