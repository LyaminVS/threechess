from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.index),
    path('board/test/', views.test),
]
