from django.urls import path
from . import views

urlpatterns = [
    path('board/<room_code>/', views.index),
    path('board/<room_code>/check_user/', views.check_user),
    path('board/<room_code>/get_color/', views.get_color)
]
