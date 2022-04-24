import consts


class Horse:

    def __init__(self, letter, number, color):
        self.letter = letter
        self.number = number
        self.position = letter + number
        self.cell = letter + number
        self.color = color

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
        cells = [check(self.position, "top", "top", "right"),
                 check(self.position, "top", "top", "left"),
                 check(self.position, "right", "right", "top"),
                 check(self.position, "right", "right", "bottom"),
                 check(self.position, "bottom", "bottom", "right"),
                 check(self.position, "bottom", "bottom", "left"),
                 check(self.position, "left", "left", "top"),
                 check(self.position, "left", "left", "bottom")]

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
