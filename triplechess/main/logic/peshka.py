from .figure import *
from .consts import *


class Peshka(Figure):
    def __init__(self, cell, color, on_road=False):
        super(Peshka, self).__init__(cell, color)
        self.__div_cells__()
        self.__first_n_zero_cells__()
        self.type = "Peshka"

    def __first_n_zero_cells__(self):
        self.first_red = []
        self.first_black = []
        self.first_white = []
        self.zero_red = []
        self.zero_black = []
        self.zero_white = []
        for let in LETTERS_1 + LETTERS_3:
            self.first_red.append(let + "11")
        for let in LETTERS_2 + LETTERS_3:
            self.first_black.append(let + "7")
        for let in LETTERS_1 + LETTERS_2:
            self.first_white.append(let + "2")
        for let in LETTERS_1 + LETTERS_3:
            self.zero_red.append(let + "12")
        for let in LETTERS_2 + LETTERS_3:
            self.zero_black.append(let + "8")
        for let in LETTERS_1 + LETTERS_2:
            self.zero_white.append(let + "1")

    def __div_cells__(self):
        self.red = []
        self.black = []
        self.white = []
        for let in LETTERS_1 + LETTERS_3:
            for n in NUMBERS_3:
                self.red.append(let + n)
        for let in LETTERS_2 + LETTERS_3:
            for n in NUMBERS_2:
                self.black.append(let + n)
        for let in LETTERS_1 + LETTERS_2:
            for n in NUMBERS_1:
                self.white.append(let + n)

    def __check_3_cells__(self, forward, forward_left, forward_right, white, black, red, grey):
        dots = []
        dots_eat = []
        dots_eat_temp, dots_temp, dots_save_temp = self.__check__(getattr(self.cell, forward)[0], white, black, red,
                                                                  grey)
        dots += dots_temp
        for c in getattr(self.cell, forward_left):
            dots_eat_temp, dots_temp, dots_save_temp = self.__check__(c, white, black, red, grey)
            dots_eat += dots_eat_temp
        for c in getattr(self.cell, forward_right):
            dots_eat_temp, dots_temp, dots_save_temp = self.__check__(c, white, black, red, grey)
            dots_eat += dots_eat_temp
        return dots, dots_eat

    def __dots__(self, white, black, red, grey):
        dots_eat = []
        dots = []
        dots_replace = []
        if self.color == "white":
            dots_temp, dots_eat_temp = self.__check_3_cells__("top", "left_top", "right_top", white, black, red, grey)
            dots += dots_temp
            dots_eat += dots_eat_temp
            if self.cell.cell[0] in self.first_white and not(self.cell.top[0] in white or self.cell.top[0] in black or self.cell.top[0] in red or self.cell.top[0] in grey):
                dots_eat_temp, dots_temp, dots_save_temp = self.__check__(f(self.cell.top[0]).top[0], white, black, red,
                                                                          grey)
                dots += dots_temp
            if self.cell.cell[0] in self.zero_black or self.cell.cell[0] in self.zero_red:
                dots_replace.append(self.cell.cell[0])
                self.on_road = True
        if self.color == "black":
            if self.cell.cell[0] in self.zero_white or self.cell.cell[0] in self.zero_red:
                dots_replace.append(self.cell.cell[0])
                self.on_road = True
            if self.cell.cell[0] in self.red:

                dots_temp, dots_eat_temp = self.__check_3_cells__("top", "left_top", "right_top", white, black, red,
                                                                  grey)
                dots += dots_temp
                dots_eat += dots_eat_temp
            else:

                dots_temp, dots_eat_temp = self.__check_3_cells__("bottom", "left_bottom", "right_bottom", white, black,
                                                                  red, grey)
                dots += dots_temp
                dots_eat += dots_eat_temp
                if self.cell.cell[0] in self.first_black and not(self.cell.bottom[0] in white or self.cell.bottom[0] in black or self.cell.bottom[0] in red or self.cell.bottom[0] in grey):
                    dots_eat_temp, dots_temp, dots_save_temp = self.__check__(f(self.cell.bottom[0]).bottom[0], white,
                                                                              black,
                                                                              red, grey)
                    dots += dots_temp
        if self.color == "red":
            if self.cell.cell[0] in self.zero_black or self.cell.cell[0] in self.zero_white:
                dots_replace.append(self.cell.cell[0])
                self.on_road = True
            if self.cell.cell[0] in self.black:
                dots_temp, dots_eat_temp = self.__check_3_cells__("top", "left_top", "right_top", white, black, red,
                                                                  grey)
                dots += dots_temp
                dots_eat += dots_eat_temp
            else:
                dots_temp, dots_eat_temp = self.__check_3_cells__("bottom", "left_bottom", "right_bottom", white, black,
                                                                  red, grey)
                dots += dots_temp
                dots_eat += dots_eat_temp
                if self.cell.cell[0] in self.first_red and not(self.cell.bottom[0] in white or self.cell.bottom[0] in black or self.cell.bottom[0] in red or self.cell.bottom[0] in grey):
                    dots_eat_temp, dots_temp, dots_save_temp = self.__check__(f(self.cell.bottom[0]).bottom[0], white,
                                                                              black,
                                                                              red, grey)
                    dots += dots_temp
        return dots, dots_eat, dots_replace
