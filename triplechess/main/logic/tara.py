import consts

class Tara:
    def __init__(self, letter, number, color):
        self.letter = letter
        self.number = number
        self.color = color
        self.is_walked = False

    # метод, который возвращает два массива:
    # массив1 - массив точек, на которые можно ходить
    # массив2 - массив точек, которые эта фигура может съесть
    # входные данные - массивы точек вида [["A", "1"], ["E", "2"],...]

    def __dots__(self, white, black, red, grey):
        numbers = []
        if self.letter in consts.LETTERS_1:
            numbers += consts.NUMBERS_1 + consts.NUMBERS_3
        if self.letter in consts.LETTERS_2:
            numbers += consts.NUMBERS_1 + consts.NUMBERS_2
        if self.letter in consts.LETTERS_3:
            numbers += consts.NUMBERS_2 + consts.NUMBERS_3

        letters = []
        if self.number in consts.NUMBERS_1:
            letters += consts.LETTERS_1 + consts.LETTERS_2
        if self.number in consts.NUMBERS_2:
            letters += consts.LETTERS_2 + consts.LETTERS_3
        if self.number in consts.NUMBERS_3:
            letters += consts.LETTERS_1 + consts.LETTERS_3
        dots = []
        dots_eat = []
        index_letter = letters.index(self.letter)
        index_number = numbers.index(self.number)
        for step in range(-1, 2, 2):
            for i in range(index_letter+step, len(letters), step):
                if [letters[i], self.number] in white:
                    if self.color != "white":
                        dots_eat.append([letters[i], self.number])
                        break
                elif [letters[i], self.number] in black:
                    if self.color != "black":
                        dots_eat.append([letters[i], self.number])
                        break
                elif [letters[i], self.number] in red:
                    if self.color != "red":
                        dots_eat.append([letters[i], self.number])
                        break
                elif [letters[i], self.number] in grey:
                    if self.color != "grey":
                        dots_eat.append([letters[i], self.number])
                        break
                else:
                    dots.append([letters[i], self.number])

        for step in range(-1, 2, 2):
            for i in range(index_number+step, len(numbers), step):
                if [self.letter, numbers[i]] in white:
                    if self.color != "white":
                        dots_eat.append([self.letter, numbers[i]])
                        break
                elif [self.letter, numbers[i]] in black:
                    if self.color != "black":
                        dots_eat.append([self.letter, numbers[i]])
                        break
                elif [self.letter, numbers[i]] in red:
                    if self.color != "red":
                        dots_eat.append([self.letter, numbers[i]])
                        break
                elif [self.letter, numbers[i]] in grey:
                    if self.color != "grey":
                        dots_eat.append([self.letter, numbers[i]])
                        break
                else:
                    dots.append([self.letter, numbers[i]])

        return dots, dots_eat
