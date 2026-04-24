from django.urls import path

from . import views

urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("user/password/", views.password_change_view, name="password_change"),
    path("user/<int:user_id>/", views.profile, name="profile"),
]
