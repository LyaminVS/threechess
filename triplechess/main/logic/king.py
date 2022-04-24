import consts

class King:
    def __init__(self, cell, color):
        self.letter = cell[0]
        self.number = cell[1::len(cell)]
        self.cell = cell
        self.is_walked = False

    def __transform_position(self, cell):
        self.letter = cell[0]
        self.number = cell[1::len(cell)]
        self.cell = cell

    def __dots__(self, white, black, red, grey):
        cells = []
        cells += getattr(getattr(consts.BOARD_RULES, self.position), "top")
        cells += getattr(getattr(consts.BOARD_RULES, self.position), "right")
        cells += getattr(getattr(consts.BOARD_RULES, self.position), "left")
        cells += getattr(getattr(consts.BOARD_RULES, self.position), "bottom")
        cells += getattr(getattr(consts.BOARD_RULES, self.position), "right_top")
        cells += getattr(getattr(consts.BOARD_RULES, self.position), "right_bottom")
        cells += getattr(getattr(consts.BOARD_RULES, self.position), "left_top")
        cells += getattr(getattr(consts.BOARD_RULES, self.position), "left_bottom")

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