import tara
import officer


class Board:
    def __init__(self):
        self.white = ["A12"]
        self.black = []
        self.red = []
        self.officer = officer.Officer("A", "12", "white")
        self.tara = tara.Tara("A", "12", "black")

board = Board()

print(board.officer.__dots__(["A12"],["K5"],[],[]))
print(board.tara.__dots__([["A", "12"]], [["A"], ["11"]] ,[],[]))





