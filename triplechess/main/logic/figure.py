import consts


class Figure:
    def __init__(self, letter, number, color):
        self.color = color
        self.cell = consts.f(letter + number)

    def __check__(self, cell, white, black, red, grey):
        dots_save_temp = []
        dots_eat_temp = []
        dots_temp = []
        if cell != '':
            colors = [white, black, red, grey]
            colors_str = ["white", "black", "red", "grey"]
            k = 0
            for i in range(4):
                if cell in colors[i]:
                    k = 1
                    if self.color != colors_str[i]:
                        dots_eat_temp.append(cell)
                    else:
                        dots_save_temp.append(cell)
            if k == 0:
                dots_temp.append(cell)
        return dots_eat_temp, dots_temp, dots_save_temp

    @staticmethod
    def __not_in_array__(c, dots, dots_eat, dots_save):
        return not (c in dots) and not (c in dots_eat) and not (c in dots_save)

    @staticmethod
    def __turn_dir__(d):
        return consts.TURN_DIR[d]