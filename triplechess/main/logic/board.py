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
        self.white_cells = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "E1", "E2", "F1", "F2", "G1", "G2", "H1",
                            "H2"]

        self.king_black = king.King("K8", "black")
        self.queen_black = queen.Queen("E8", "black")
        self.horse_black_1 = horse.Horse("M8", "black")
        self.horse_black_2 = horse.Horse("G8", "black")
        self.officer_black_1 = officer.Officer("L8", "black")
        self.officer_black_2 = officer.Officer("F8", "black")
        self.tara_black_1 = tara.Tara("N8", "black")
        self.tara_black_2 = tara.Tara("H8", "black")
        self.peshka_black_1 = peshka.Peshka("H7", "black")
        self.peshka_black_2 = peshka.Peshka("G7", "black")
        self.peshka_black_3 = peshka.Peshka("F7", "black")
        self.peshka_black_4 = peshka.Peshka("E7", "black")
        self.peshka_black_5 = peshka.Peshka("K7", "black")
        self.peshka_black_6 = peshka.Peshka("L7", "black")
        self.peshka_black_7 = peshka.Peshka("M7", "black")
        self.peshka_black_8 = peshka.Peshka("N7", "black")
        self.black = [self.king_black, self.queen_black, self.horse_black_1, self.horse_black_2,
                      self.officer_black_1, self.officer_black_2, self.tara_black_1, self.tara_black_2,
                      self.peshka_black_1, self.peshka_black_2, self.peshka_black_3, self.peshka_black_4,
                      self.peshka_black_5, self.peshka_black_6, self.peshka_black_7, self.peshka_black_8]
        self.black_cells = ["H8", "H7", "G8", "G7", "F8", "F7", "E8", "E7", "K8", "K7", "L8", "L7", "M8", "M7", "N8",
                            "N7"]

        self.king_red = king.King("D12", "red")
        self.queen_red = queen.Queen("K12", "red")
        self.horse_red_1 = horse.Horse("B12", "red")
        self.horse_red_2 = horse.Horse("M12", "red")
        self.officer_red_1 = officer.Officer("C12", "red")
        self.officer_red_2 = officer.Officer("L12", "red")
        self.tara_red_1 = tara.Tara("A12", "red")
        self.tara_red_2 = tara.Tara("N12", "red")
        self.peshka_red_1 = peshka.Peshka("A11", "red")
        self.peshka_red_2 = peshka.Peshka("B11", "red")
        self.peshka_red_3 = peshka.Peshka("C11", "red")
        self.peshka_red_4 = peshka.Peshka("D11", "red")
        self.peshka_red_5 = peshka.Peshka("K11", "red")
        self.peshka_red_6 = peshka.Peshka("L11", "red")
        self.peshka_red_7 = peshka.Peshka("M11", "red")
        self.peshka_red_8 = peshka.Peshka("N11", "red")
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
        if color=="white":
            king_position = self.king_white.cell
            figures_1 = self.black
            figures_2 = self.red
        else if color=="black":
            king_position = self.king_black.cell
            figures_1 = self.white
            figures_2 = self.red
        else if color=="red":
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
