from .consts import *
from .figure import Figure


class King(Figure):
    def __init__(self, cell, color):
        super(King, self).__init__(cell, color)
        self.is_walked = False
        self.type = "King"



    def __dots__(self, white, black, red, grey):
        cells = []
        cells += getattr(getattr(BOARD_RULES, self.cell_str), "top")
        cells += getattr(getattr(BOARD_RULES, self.cell_str), "right")
        cells += getattr(getattr(BOARD_RULES, self.cell_str), "left")
        cells += getattr(getattr(BOARD_RULES, self.cell_str), "bottom")
        cells += getattr(getattr(BOARD_RULES, self.cell_str), "right_top")
        cells += getattr(getattr(BOARD_RULES, self.cell_str), "right_bottom")
        cells += getattr(getattr(BOARD_RULES, self.cell_str), "left_top")
        cells += getattr(getattr(BOARD_RULES, self.cell_str), "left_bottom")

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
