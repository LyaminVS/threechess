import tara
import officer
import peshka
import queen
import king
import horse

class Board:
    def __init__(self):
        self.king_white = king.King("E1", "white")
        self.queen_white = queen.Queen("D1", "white")
        self.horse_white_1 = horse.Horse("C1", "white")
        self.horse_white_2 = horse.Horse("F1", "white")
        self.officer_white_1 = officer.Officer("B1", "white")
        self.officer_white_2 = officer.Officer("G1", "white")
        self.tara_white_1 = tara.Tara("A1", "white")
        self.tara_white_2 = tara.Tara("H1", "white")
        self.peshka_white_1 = peshka.Peshka("A2", "white")
        self.peshka_white_2 = peshka.Peshka("B2", "white")
        self.peshka_white_3 = peshka.Peshka("C2", "white")
        self.peshka_white_4 = peshka.Peshka("D2", "white")
        self.peshka_white_5 = peshka.Peshka("E2", "white")
        self.peshka_white_6 = peshka.Peshka("F2", "white")
        self.peshka_white_7 = peshka.Peshka("G2", "white")
        self.peshka_white_8 = peshka.Peshka("H2", "white")
        self.white = [self.king_white, self.queen_white, self.horse_white_1, self.horse_white_2,
                      self.officer_white_1, self.officer_white_2, self.tara_white_1, self.tara_white_2,
                      self.peshka_white_1, self.peshka_white_2, self.peshka_white_3, self.peshka_white_4,
                      self.peshka_white_5, self.peshka_white_6, self.peshka_white_7, self.peshka_white_8]
        self.white_cells = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "E1", "E2", "F1", "F2", "G1", "G2", "H1", "H2"]




    # def __king_is_checked__(self, color):
    #     if color=="white":
    #         king_position = self.king_white.cell
    #         figures_1 = self.black
    #         figures_2 = self.red
    #     if color=="black":
    #         king_position = self.king_black.cell
    #         figures_1 = self.white
    #         figures_2 = self.red
    #     if color=="red":
    #         king_position = self.king_red.cell
    #         figures_1 = self.black
    #         figures_2 = self.white
    #
    #     for elem in figures_1:
    #         if king_position in elem.__dots__(self.white_cells, self.black_cells, self.red_cells, self.grey_cells)[1]:
    #             return True
    #     for elem in figures_1:
    #         if king_position in elem.__dots__(self.white_cells, self.black_cells, self.red_cells, self.grey_cells)[1]:
    #             return True
    #     return False




board = Board()

print(board.queen_white.__dots__([], [], [], []))
# print(board.officer.__dots__(["A12"],["L6"],[],[]))
# print(board.tara.__dots__(["K9"], ["L9", "D9", "K10"] ,[],[]))

