# import officer
# import tara
from .officer import *
from .tara import *
from .consts import *


class Queen(Officer, Tara):
    def __init__(self, cell, color):
        super(Queen, self).__init__(cell, color)

    def __dots__(self, white, black, red, grey):
        dots = []
        dots_eat = []
        dots_temp, dots_eat_temp = Officer.__dots__(self, white, black, red, grey)
        dots += dots_temp
        dots_eat += dots_eat
        dots_temp, dots_eat_temp = Tara.__dots__(self, white, black, red, grey)
        dots += dots_temp
        dots_eat += dots_eat
        return dots, dots_eat
