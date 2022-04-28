# import consts
from .consts import *

class King:
    def __init__(self, cell, color):
        self.letter = cell[0]
        self.number = cell[1:len(cell)]
        self.cell = cell
        self.color = color
        self.is_walked = False

    def __transform_position(self, cell):
        self.letter = cell[0]
        self.number = cell[1::len(cell)]
        self.cell = cell

    def __dots__(self, white, black, red, grey):
        cells = []
        cells += getattr(getattr(BOARD_RULES, self.cell), "top")
        cells += getattr(getattr(BOARD_RULES, self.cell), "right")
        cells += getattr(getattr(BOARD_RULES, self.cell), "left")
        cells += getattr(getattr(BOARD_RULES, self.cell), "bottom")
        cells += getattr(getattr(BOARD_RULES, self.cell), "right_top")
        cells += getattr(getattr(BOARD_RULES, self.cell), "right_bottom")
        cells += getattr(getattr(BOARD_RULES, self.cell), "left_top")
        cells += getattr(getattr(BOARD_RULES, self.cell), "left_bottom")

        dots = []
        dots_eat = []
        for cell in cells:
            if cell in white:
                if self.color != "white":
                    dots_eat.append(cell)
            elif cell in black:
                if self.color != "black":
                    dots_eat.append(cell)
            elif cell in red:
                if self.color != "red":
                    dots_eat.append(cell)
            elif cell in grey:
                if self.color != "grey":
                    dots_eat.append(cell)
            elif cell != "":
                dots.append(cell)



        return dots, dots_eat