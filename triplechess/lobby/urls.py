from django.urls import path
from . import views

urlpatterns = [
    path('lobby/', views.index),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('', views.on_open)
]
