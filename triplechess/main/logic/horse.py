import consts


class Horse:

    def __init__(self, cell, color):
        self.letter = cell[0]
        self.number = cell[1:len(cell)]
        self.cell = cell
        self.color = color

    def __transform_position(self, cell):
        self.letter = cell[0]
        self.number = cell[1::len(cell)]
        self.cell = cell


    def __dots__(self, white, black, red, grey):

        def check(position, str1, str2, str3):
            cell = getattr(getattr(consts.BOARD_RULES, position), str1)
            if cell[0] == "": return ""
            cell = getattr(getattr(consts.BOARD_RULES, cell[0]), str2)
            if cell[0] == "": return ""
            cell = getattr(getattr(consts.BOARD_RULES, cell[0]), str3)

            return cell[0]

        dots = []
        dots_eat = []
        cells = [check(self.cell, "top", "top", "right"),
                 check(self.cell, "top", "top", "left"),
                 check(self.cell, "right", "right", "top"),
                 check(self.cell, "right", "right", "bottom"),
                 check(self.cell, "bottom", "bottom", "right"),
                 check(self.cell, "bottom", "bottom", "left"),
                 check(self.cell, "left", "left", "top"),
                 check(self.cell, "left", "left", "bottom")]

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
