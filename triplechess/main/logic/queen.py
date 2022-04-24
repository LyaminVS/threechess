import officer
import tara


class Queen(officer.Officer, tara.Tara):
    def __init__(self, letter, number, color):
        super(Queen, self).__init__(letter, number, color)

    def __dots__(self, white, black, red, grey):
        dots = []
        dots_eat = []
        dots_temp, dots_eat_temp = officer.Officer.__dots__(self, white, black, red, grey)
        dots += dots_temp
        dots_eat += dots_eat
        dots_temp, dots_eat_temp = tara.Tara.__dots__(self, white, black, red, grey)
        dots += dots_temp
        dots_eat += dots_eat
        return dots, dots_eat
