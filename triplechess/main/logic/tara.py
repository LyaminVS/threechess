import consts

class Tara:
    def __init__(self, letter, number, color):
        self.letter = letter
        self.number = number
        self.color = "red"

    def __dots__(self, white, black, red):
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
        for i in range(letter, )


