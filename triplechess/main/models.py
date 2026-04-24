from django.db import models
from django.conf import settings


# Create your models here.


class Game(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_games",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player_1", on_delete=models.PROTECT, null=True)
    player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player_2", on_delete=models.PROTECT, null=True)
    player_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player_3", on_delete=models.PROTECT, null=True)

    color_1 = models.CharField(max_length=10, default="random")
    color_2 = models.CharField(max_length=10, default="random")
    color_3 = models.CharField(max_length=10, default="random")

    ready_1 = models.IntegerField(default=0)
    ready_2 = models.IntegerField(default=0)
    ready_3 = models.IntegerField(default=0)

    disconnected_1 = models.CharField(max_length=20, default="connected")
    disconnected_2 = models.CharField(max_length=20, default="connected")
    disconnected_3 = models.CharField(max_length=20, default="connected")

    board = models.TextField()

    status = models.CharField(max_length=50, default="")

    # Режим песочницы: только суперпользователь, без очереди хода, все три цвета с одной учётки
    is_sandbox = models.BooleanField(default=False)
    # Приватная партия владельца, не показывается другим в лобби
    is_private = models.BooleanField(default=False)
    # Для песочницы: False = без очереди, True = классический порядок хода
    sandbox_ordered_turn = models.BooleanField(default=False)

    @classmethod
    def create(cls, player_1, player_2, player_3, board):
        game = cls(status="in_lobby", player_1=player_1, player_2=player_2, player_3=player_3, board=board)
        return game
