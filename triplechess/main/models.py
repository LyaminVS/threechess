from django.db import models
from django.conf import settings


# Create your models here.


class Game(models.Model):
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player_1", on_delete=models.CASCADE)
    player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player_2", on_delete=models.CASCADE)
    player_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player_3", on_delete=models.CASCADE)

    board = models.TextField()

    status = models.CharField(max_length=50, default="")

    @classmethod
    def create(cls, player_1, player_2, player_3, board):
        game = cls(status="in_lobby", player_1=player_1, player_2=player_2, player_3=player_3, board=board)
        return game
