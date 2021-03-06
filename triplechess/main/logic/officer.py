from .figure import *


class Officer(Figure):
    def __init__(self, cell, color):
        super(Officer, self).__init__(cell, color)
        self.type = "Officer"

    def __iteration__(self, cell, white, black, red, grey, dots_eat, dots, dots_save, d):
        dots_eat_temp, dots_temp, dots_save_temp = self.__check__(cell, white, black, red, grey)
        dots_eat += dots_eat_temp
        dots += dots_temp
        turned_d = self.__turn_dir__(d)
        dots_save += dots_save_temp
        if not (cell in dots_eat) and not (cell in dots_save) and cell != '':
            cell = f(cell)
            for c_child in getattr(cell, d):
                if self.__not_in_array__(c_child, dots, dots_eat, dots_save):
                    self.__iteration__(c_child, white, black, red, grey, dots_eat, dots, dots_save, d)
            for c_child in getattr(cell, turned_d):
                if self.__not_in_array__(c_child, dots, dots_eat, dots_save):
                    self.__iteration__(c_child, white, black, red, grey, dots_eat, dots, dots_save, turned_d)

    def __dots__(self, white, black, red, grey):
        dots_eat = []
        dots = []
        dots_save = []
        dirs = ["right_bottom", "left_top", "right_top", "left_bottom"]
        for d in dirs:
            for cell in getattr(self.cell, d):
                self.__iteration__(cell, white, black, red, grey, dots_eat, dots, dots_save, d)
        return dots, dots_eat
