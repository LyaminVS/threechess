import consts
from consts import f
import figure

class Peshka(figure.Figure):
    def __init__(self, letter, number, color):
        super(Peshka, self,).__init__(letter, number, color)
        self.__div_cells__()

    def __div_cells__(self):
        self.red = []
        self.black = []
        self.white = []
        for l in consts.LETTERS_1 + consts.LETTERS_3:
            for n in consts.NUMBERS_3:
                self.red.append(l + n)
        for l in consts.LETTERS_2 + consts.LETTERS_3:
            for n in consts.NUMBERS_2:
                self.red.append(l + n)
        for l in consts.LETTERS_1 + consts.LETTERS_2:
            for n in consts.NUMBERS_1:
                self.red.append(l + n)

    # def __turn_cell__(self, cell):
    #     if self.color == "black":
    #         if (cell.cell in self.black) or(cell.cell in self.white):
    #             for d in consts.TURN_DIR.items():
    #                 getattr(d) = getattr(d)




    def __dots__(self, white, black, red, grey):
        dots_eat = []
        dots = []
        dots_save = []


