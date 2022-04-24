import tara
import officer


class Board:
    def __init__(self):
        self.white = ["A12"]
        self.black = []
        self.red = []
        self.officer = officer.Officer("D", "9", "white")
        self.tara = tara.Tara("A", "12", "black")


board = Board()

print(board.officer.__dots__(["D9"],[""],[],[]))
print(board.tara.__dots__([["A", "12"]], [["A"], ["11"]] ,[],[]))





