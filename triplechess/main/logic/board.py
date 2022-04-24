import tara
import officer
import peshka

class Board:
    def __init__(self):
        self.white = ["A12"]
        self.black = []
        self.red = []
        self.officer = officer.Officer("A", "12", "white")
        self.tara = tara.Tara("K", "9", "white")
        self.peshka = peshka.Peshka("E", "1", "red")

board = Board()

print(board.peshka.__dots__(["B2"], ["E4", "K5"], [""], []))
# print(board.officer.__dots__(["A12"],["L6"],[],[]))
# print(board.tara.__dots__(["K9"], ["L9", "D9", "K10"] ,[],[]))

