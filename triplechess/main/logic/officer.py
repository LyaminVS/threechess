from consts import f


class Officer:
    def __init__(self, letter, number, color):
        self.color = color
        self.cell = f(letter + number)

    @staticmethod
    def __not_in_array__(c, dots, dots_eat, dots_save):
        return not (c in dots) and not (c in dots_eat) and not (c in dots_save)

    @staticmethod
    def __turn_dir__(d):
        if d == "right_bottom":
            d = "left_top"
        elif d == "right_top":
            d = "left_bottom"
        elif d == "left_bottom":
            d = "right_top"
        elif d == "left_top":
            d = "right_bottom"
        return d

    def __check__(self, cell, white, black, red, grey):
        dots_save_temp = []
        dots_eat_temp = []
        dots_temp = []
        for c in cell:
            if c != '':
                c = f(c)
                colors = [white, black, red, grey]
                colors_str = ["white", "black", "red", "grey"]
                k = 0
                for i in range(4):
                    if c.cell[0] in colors[i]:
                        k = 1
                        if self.color != colors_str[i]:
                            dots_eat_temp = dots_eat_temp + c.cell
                        else:
                            dots_save_temp = dots_save_temp + c.cell
                if k == 0:
                    dots_temp = dots_temp + c.cell
        return dots_eat_temp, dots_temp, dots_save_temp

    def __iteration__(self, cell, white, black, red, grey, dots_eat, dots, dots_save, d):
        dots_eat_temp, dots_temp, dots_save_temp = self.__check__(cell, white, black, red, grey)
        dots_eat += dots_eat_temp
        dots += dots_temp
        turned_dir = self.__turn_dir__(d)
        dots_save += dots_save_temp
        for c in cell:
            if not (c in dots_eat) and not (c in dots_save) and c != '':
                c = f(c)
                for c_child in getattr(c, d):
                    if self.__not_in_array__(c_child, dots, dots_eat, dots_save):
                        self.__iteration__([c_child], white, black, red, grey, dots_eat, dots, dots_save, d)
                for c_child in getattr(c, turned_dir):
                    if self.__not_in_array__(c_child, dots, dots_eat, dots_save):
                        self.__iteration__([c_child], white, black, red, grey, dots_eat, dots, dots_save, turned_dir)

    def __dots__(self, white, black, red, grey):
        dots_eat = []
        dots = []
        dots_save = []
        dirs = ["right_bottom", "left_top", "right_top", "left_bottom"]
        for d in dirs:
            self.__iteration__(getattr(self.cell, d), white, black, red, grey, dots_eat, dots, dots_save, d)
        return dots, dots_eat
