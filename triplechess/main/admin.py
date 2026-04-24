from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "is_sandbox", "player_1", "player_2", "player_3")
    list_filter = ("status", "is_sandbox")

# Register your models here.
