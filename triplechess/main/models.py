from django.db import models
from django.conf import settings


# Create your models here.


class Board(models.Model):
    board = models.TextField()


class Game(models.Model):
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player_1", on_delete=models.CASCADE)
    player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player_2", on_delete=models.CASCADE)
    player_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="player_3", on_delete=models.CASCADE)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)