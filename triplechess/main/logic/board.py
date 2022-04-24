import tara
import officer


class Board:
    def __init__(self):
        self.white = ["A12"]
        self.black = []
        self.red = []
        self.officer = officer.Officer("A", "12", "white")
        self.tara = tara.Tara("K", "9", "white")

board = Board()

print(board.officer.__dots__(["A12"],["L6"],[],[]))
print(board.tara.__dots__(["K9"], ["L9", "D9", "K10"] ,[],[]))

