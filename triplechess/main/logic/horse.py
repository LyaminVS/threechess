from .consts import *
from .figure import Figure


class Horse(Figure):
    def __init__(self, cell, color):
        super(Horse, self).__init__(cell, color)
        self.type = "Horse"

    def __transform_position(self, cell):
        self.letter = cell[0]
        self.number = cell[1::len(cell)]
        self.cell_str = cell

    def __dots__(self, white, black, red, grey):

        def check(position, str1, str2, str3):
            c = getattr(getattr(BOARD_RULES, position), str1)
            if c[0] == "":
                return ""
            c = getattr(getattr(BOARD_RULES, c[0]), str2)
            if c[0] == "":
                return ""
            c = getattr(getattr(BOARD_RULES, c[0]), str3)
            return c[0]

        dots = []
        dots_eat = []
        cells = [check(self.cell_str, "top", "top", "right"),
                 check(self.cell_str, "top", "top", "left"),
                 check(self.cell_str, "right", "right", "top"),
                 check(self.cell_str, "right", "right", "bottom"),
                 check(self.cell_str, "bottom", "bottom", "right"),
                 check(self.cell_str, "bottom", "bottom", "left"),
                 check(self.cell_str, "left", "left", "top"),
                 check(self.cell_str, "left", "left", "bottom")]

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
