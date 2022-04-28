# import tara
# import officer
# import peshka
# import queen
# import king
# import horse
from .tara import Tara as Tara
from .officer import Officer as Officer
from .peshka import Peshka as Peshka
from .queen import Queen as Queen
from .king import King as King
from .horse import Horse as Horse


class Board:
    def __init__(self):
        self.king_white = King("E1", "white")
        self.queen_white = Queen("D1", "white")
        self.horse_white_1 = Horse("C1", "white")
        self.horse_white_2 = Horse("F1", "white")
        self.officer_white_1 = Officer("B1", "white")
        self.officer_white_2 = Officer("G1", "white")
        self.tara_white_1 = Tara("A1", "white")
        self.tara_white_2 = Tara("H1", "white")
        self.peshka_white_1 = Peshka("A2", "white")
        self.peshka_white_2 = Peshka("B2", "white")
        self.peshka_white_3 = Peshka("C2", "white")
        self.peshka_white_4 = Peshka("D2", "white")
        self.peshka_white_5 = Peshka("E2", "white")
        self.peshka_white_6 = Peshka("F2", "white")
        self.peshka_white_7 = Peshka("G2", "white")
        self.peshka_white_8 = Peshka("H2", "white")
        self.white = [self.king_white, self.queen_white, self.horse_white_1, self.horse_white_2,
                      self.officer_white_1, self.officer_white_2, self.tara_white_1, self.tara_white_2,
                      self.peshka_white_1, self.peshka_white_2, self.peshka_white_3, self.peshka_white_4,
                      self.peshka_white_5, self.peshka_white_6, self.peshka_white_7, self.peshka_white_8]
        self.white_cells = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "E1", "E2", "F1", "F2", "G1", "G2", "H1",
                            "H2"]

        self.king_black = King("K8", "black")
        self.queen_black = Queen("E8", "black")
        self.horse_black_1 = Horse("M8", "black")
        self.horse_black_2 = Horse("G8", "black")
        self.officer_black_1 = Officer("L8", "black")
        self.officer_black_2 = Officer("F8", "black")
        self.tara_black_1 = Tara("N8", "black")
        self.tara_black_2 = Tara("H8", "black")
        self.peshka_black_1 = Peshka("H7", "black")
        self.peshka_black_2 = Peshka("G7", "black")
        self.peshka_black_3 = Peshka("F7", "black")
        self.peshka_black_4 = Peshka("E7", "black")
        self.peshka_black_5 = Peshka("K7", "black")
        self.peshka_black_6 = Peshka("L7", "black")
        self.peshka_black_7 = Peshka("M7", "black")
        self.peshka_black_8 = Peshka("N7", "black")
        self.black = [self.king_black, self.queen_black, self.horse_black_1, self.horse_black_2,
                      self.officer_black_1, self.officer_black_2, self.tara_black_1, self.tara_black_2,
                      self.peshka_black_1, self.peshka_black_2, self.peshka_black_3, self.peshka_black_4,
                      self.peshka_black_5, self.peshka_black_6, self.peshka_black_7, self.peshka_black_8]
        self.black_cells = ["H8", "H7", "G8", "G7", "F8", "F7", "E8", "E7", "K8", "K7", "L8", "L7", "M8", "M7", "N8",
                            "N7"]

        self.king_red = King("D12", "red")
        self.queen_red = Queen("K12", "red")
        self.horse_red_1 = Horse("B12", "red")
        self.horse_red_2 = Horse("M12", "red")
        self.officer_red_1 = Officer("C12", "red")
        self.officer_red_2 = Officer("L12", "red")
        self.tara_red_1 = Tara("A12", "red")
        self.tara_red_2 = Tara("N12", "red")
        self.peshka_red_1 = Peshka("A11", "red")
        self.peshka_red_2 = Peshka("B11", "red")
        self.peshka_red_3 = Peshka("C11", "red")
        self.peshka_red_4 = Peshka("D11", "red")
        self.peshka_red_5 = Peshka("K11", "red")
        self.peshka_red_6 = Peshka("L11", "red")
        self.peshka_red_7 = Peshka("M11", "red")
        self.peshka_red_8 = Peshka("N11", "red")
        self.red = [self.king_red, self.queen_red, self.horse_red_1, self.horse_red_2,
                    self.officer_red_1, self.officer_red_2, self.tara_red_1, self.tara_red_2,
                    self.peshka_red_1, self.peshka_red_2, self.peshka_red_3, self.peshka_red_4,
                    self.peshka_red_5, self.peshka_red_6, self.peshka_red_7, self.peshka_red_8]
        self.red_cells = ["A12", "A11", "B12", "B11", "C12", "C11", "D12", "D11", "K12", "K11", "L12", "L11", "M12",
                            "M11", "N12", "N11"]

        self.grey = []
        self.grey_cells = []
        self.all_figures = self.white + self.black + self.red

    def get_dots(self, cell):
        for figure in self.all_figures:
            if figure.letter + figure.number == cell:
                dots = figure.__dots__(self.white_cells, self.black_cells, self.red_cells, [])
                return dots
    def __king_is_checked__(self, color):
        king_position = ""
        figures_1 = []
        figures_2 = []


        if color=="white":
            king_position = self.king_white.cell
            figures_1 = self.black
            figures_2 = self.red
        elif color=="black":
            king_position = self.king_black.cell
            figures_1 = self.white
            figures_2 = self.red
        elif color=="red":
            king_position = self.king_red.cell
            figures_1 = self.black
            figures_2 = self.white

        for elem in figures_1:
            if king_position in elem.__dots__(self.white_cells, self.black_cells, self.red_cells, self.grey_cells)[1]:
                return True
        for elem in figures_2:
            if king_position in elem.__dots__(self.white_cells, self.black_cells, self.red_cells, self.grey_cells)[1]:
                return True
        return False


board = Board()
print(board.__king_is_checked__("white"))

# print(board.queen_white.__dots__([], [], [], []))
# print(board.officer.__dots__(["A12"],["L6"],[],[]))
# print(board.tara.__dots__(["K9"], ["L9", "D9", "K10"] ,[],[]))
