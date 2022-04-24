import tara
import officer
import horse

class Board:
    def __init__(self):
        self.white = ["A12"]
        self.black = []
        self.red = []
        self.officer = officer.Officer("A", "12", "white")
        self.tara = tara.Tara("K", "9", "white")
        self.horse = horse.Horse("A", "1", "white")

board = Board()
print(board.horse.__dots__(["E4", "B3"],[],[],[]))

