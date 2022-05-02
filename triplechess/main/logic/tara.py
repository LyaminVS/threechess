from .consts import *
from .figure import Figure


class Tara(Figure):
    def __init__(self, cell, color):
        super(Tara, self).__init__(cell, color)
        self.type = "Tara"

    def __transform_position(self, cell):
        self.letter = cell[0]
        self.number = cell[1::len(cell)]
        self.cell_str = cell

    # метод, который возвращает два массива:
    # массив1 - массив точек, на которые можно ходить
    # массив2 - массив точек, которые эта фигура может съесть
    # входные данные - массивы точек вида ["A1","D5"...]

    def __dots__(self, white, black, red, grey):

        def check(flag, mas):
            if flag == -1:
                return -1
            if flag == 1:
                return len(mas)

        numbers = []
        if self.letter in LETTERS_1:
            numbers = ['12', '11', '10', '9', '4', '3', '2', '1']
        if self.letter in LETTERS_2:
            numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        if self.letter in LETTERS_3:
            numbers = ['8', '7', '6', '5', '9', '10', '11', '12']

        letters = []
        if self.number in NUMBERS_1:
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        if self.number in NUMBERS_2:
            letters = ['H', 'G', 'F', 'E', 'K', 'L', 'M', 'N']
        if self.number in NUMBERS_3:
            letters = ['A', 'B', 'C', 'D', 'K', 'L', 'M', 'N']
        dots = []
        dots_eat = []
        index_letter = letters.index(self.letter)
        index_number = numbers.index(self.number)
        for step in range(-1, 2, 2):
            for i in range(index_letter + step, check(step, letters), step):
                if letters[i] + self.number in white:
                    if self.color != "white":
                        dots_eat.append(letters[i] + self.number)
                    break
                elif letters[i] + self.number in black:
                    if self.color != "black":
                        dots_eat.append(letters[i] + self.number)
                    break
                elif letters[i] + self.number in red:
                    if self.color != "red":
                        dots_eat.append(letters[i] + self.number)
                    break
                elif letters[i] + self.number in grey:
                    if self.color != "grey":
                        dots_eat.append(letters[i] + self.number)
                    break
                else:
                    dots.append(letters[i] + self.number)

        for step in range(-1, 2, 2):
            for i in range(index_number + step, check(step, numbers), step):
                if self.letter + numbers[i] in white:
                    if self.color != "white":
                        dots_eat.append(self.letter + numbers[i])
                    break
                elif self.letter + numbers[i] in black:
                    if self.color != "black":
                        dots_eat.append(self.letter + numbers[i])
                    break
                elif self.letter + numbers[i] in red:
                    if self.color != "red":
                        dots_eat.append(self.letter + numbers[i])
                    break
                elif self.letter + numbers[i] in grey:
                    if self.color != "grey":
                        dots_eat.append(self.letter + numbers[i])
                    break
                else:
                    dots.append(self.letter + numbers[i])

        return dots, dots_eat
