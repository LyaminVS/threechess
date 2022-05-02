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
        self.horse_white_1 = Horse("B1", "white")
        self.horse_white_2 = Horse("G1", "white")
        self.officer_white_1 = Officer("C1", "white")
        self.officer_white_2 = Officer("F1", "white")
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
        self.white_cells = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2",
                            "E1", "E2", "F1", "F2", "G1", "G2", "H1", "H2"]

        self.king_black = King("K8", "black")
        self.queen_black = Queen("E8", "black")
        self.horse_black_1 = Horse("M8", "black")
        self.horse_black_2 = Horse("G8", "black")
        self.officer_black_1 = Officer("L8", "black")
        self.officer_black_2 = Officer("F8", "black")
        self.tara_black_1 = Tara("H8", "black")
        self.tara_black_2 = Tara("N8", "black")
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
        self.black_cells = ["H8", "H7", "G8", "G7", "F8", "F7", "E8", "E7",
                            "K8", "K7", "L8", "L7", "M8", "M7", "N8", "N7"]

        self.king_red = King("D12", "red")
        self.queen_red = Queen("K12", "red")
        self.horse_red_1 = Horse("B12", "red")
        self.horse_red_2 = Horse("M12", "red")
        self.officer_red_1 = Officer("C12", "red")
        self.officer_red_2 = Officer("L12", "red")
        self.tara_red_1 = Tara("N12", "red")
        self.tara_red_2 = Tara("A12", "red")
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
        self.red_cells = ["A12", "A11", "B12", "B11", "C12", "C11", "D12", "D11",
                          "K12", "K11", "L12", "L11", "M12", "M11", "N12", "N11"]

        self.grey = []
        self.grey_cells = []
        self.all_figures = self.white + self.black + self.red

    def __king_is_checked__(self, color, cell=""):
        is_checked = False
        king_position = ""
        figures_1 = []
        figures_2 = []
        king = getattr(self, "king_" + color)
        cell_first = king.cell_str
        if color == "white":
            king_position = self.king_white.cell_str
            figures_1 = self.black
            figures_2 = self.red
        elif color == "black":
            king_position = self.king_black.cell_str
            figures_1 = self.white
            figures_2 = self.red
        elif color == "red":
            king_position = self.king_red.cell_str
            figures_1 = self.black
            figures_2 = self.white
        if cell == "":
            cell = king_position
        king.change_cell_temp(cell)
        getattr(self, color + "_cells").remove(cell_first)
        getattr(self, color + "_cells").append(cell)
        king_position = cell
        for elem in figures_1:
            if (elem.cell_str in self.red_cells) and (elem.color == "red") \
                    or (elem.cell_str in self.black_cells) and (elem.color == "black") \
                    or (elem.cell_str in self.white_cells) and (elem.color == "white"):
                if king_position in elem.__dots__(self.white_cells, self.black_cells, self.red_cells, self.grey_cells)[
                    1]:
                    is_checked = True
        for elem in figures_2:
            if (elem.cell_str in self.red_cells) and (elem.color == "red") \
                    or (elem.cell_str in self.black_cells) and (elem.color == "black") \
                    or (elem.cell_str in self.white_cells) and (elem.color == "white"):
                if king_position in elem.__dots__(self.white_cells, self.black_cells, self.red_cells, self.grey_cells)[
                    1]:
                    is_checked = True
        getattr(self, color + "_cells").remove(cell)
        getattr(self, color + "_cells").append(cell_first)
        king.change_cell_temp(cell_first)
        return is_checked

    def __update_dots__(self, figure):
        dots = figure.__dots__(self.white_cells, self.black_cells, self.red_cells, self.grey_cells)
        cell = figure.cell_str
        cell_temp = cell
        i = 0
        while i < (len(dots[0])):
            if figure.color == "white":
                self.white_cells.remove(cell_temp)
                self.white_cells.append(dots[0][i])
                figure.change_cell_temp(dots[0][i])
                cell_temp = dots[0][i]
                if self.__king_is_checked__(figure.color):
                    del dots[0][i]
                    i -= 1
            if figure.color == "black":
                self.black_cells.remove(cell_temp)
                self.black_cells.append(dots[0][i])
                figure.change_cell_temp(dots[0][i])
                cell_temp = dots[0][i]
                if self.__king_is_checked__(figure.color):
                    del dots[0][i]
                    i -= 1
            if figure.color == "red":
                self.red_cells.remove(cell_temp)
                self.red_cells.append(dots[0][i])
                figure.change_cell_temp(dots[0][i])
                cell_temp = dots[0][i]
                if self.__king_is_checked__(figure.color):
                    del dots[0][i]
                    i -= 1
            i += 1
        figure.change_cell(cell)
        if figure.color == "white":
            self.white_cells.remove(cell_temp)
            self.white_cells.append(cell)
        if figure.color == "black":
            self.black_cells.remove(cell_temp)
            self.black_cells.append(cell)
        if figure.color == "red":
            self.red_cells.remove(cell_temp)
            self.red_cells.append(cell)

        cell_temp = cell
        k = ""
        i = 0
        flag = 0
        while i < (len(dots[1])):
            if figure.color == "white":
                self.white_cells.remove(cell_temp)
                self.white_cells.append(dots[1][i])
                figure.change_cell_temp(dots[1][i])
                if dots[1][i] in self.black_cells:
                    self.black_cells.remove(dots[1][i])
                    k = "black"
                if dots[1][i] in self.red_cells:
                    self.red_cells.remove(dots[1][i])
                    k = "red"
                cell_temp = dots[1][i]
                if self.__king_is_checked__(figure.color):
                    flag = 1

                if k == "black":
                    self.black_cells.append(dots[1][i])
                    k = ""
                if k == "red":
                    self.red_cells.append(dots[1][i])
                    k = ""
                if flag == 1:
                    flag = 0
                    del dots[1][i]
                    i -= 1
            if figure.color == "black":
                self.black_cells.remove(cell_temp)
                self.black_cells.append(dots[1][i])
                figure.change_cell_temp(dots[1][i])
                if dots[1][i] in self.white_cells:
                    self.white_cells.remove(dots[1][i])
                    k = "white"
                if dots[1][i] in self.red_cells:
                    self.red_cells.remove(dots[1][i])
                    k = "red"
                cell_temp = dots[1][i]
                if self.__king_is_checked__(figure.color):
                    flag = 1
                if k == "white":
                    self.white_cells.append(dots[1][i])
                    k = ""
                if k == "red":
                    self.red_cells.append(dots[1][i])
                    k = ""
                if flag == 1:
                    flag = 0
                    del dots[1][i]
                    i -= 1

            if figure.color == "red":
                self.red_cells.remove(cell_temp)
                self.red_cells.append(dots[1][i])
                figure.change_cell_temp(dots[1][i])
                if dots[1][i] in self.black_cells:
                    self.black_cells.remove(dots[1][i])
                    k = "black"
                if dots[1][i] in self.white_cells:
                    self.white_cells.remove(dots[1][i])
                    k = "white"
                cell_temp = dots[1][i]
                if self.__king_is_checked__(figure.color):
                    flag = 1
                if k == "black":
                    self.black_cells.append(dots[1][i])
                    k = ""
                if k == "white":
                    self.white_cells.append(dots[1][i])
                    k = ""
                if flag == 1:
                    flag = 0
                    del dots[1][i]
                    i -= 1

            i += 1
        figure.change_cell(cell)
        if figure.color == "white":
            self.white_cells.remove(cell_temp)
            self.white_cells.append(cell)
        if figure.color == "black":
            self.black_cells.remove(cell_temp)
            self.black_cells.append(cell)
        if figure.color == "red":
            self.red_cells.remove(cell_temp)
            self.red_cells.append(cell)

        return dots

    def __king_is_checkmated__(self, color):
        figures = []
        if color == "white":
            figures = self.white
        if color == "black":
            figures = self.black
        if color == "red":
            figures = self.red

        is_checkmated = True
        for elem in figures:
            if self.__update_dots__(elem) != [[], []]:
                is_checkmated = False

        if self.__king_is_checked__(color):
            return is_checkmated
        else:
            return False

    def __king_is_pated__(self, color):
        figures = []
        if color == "white":
            figures = self.white
        if color == "black":
            figures = self.black
        if color == "red":
            figures = self.red

        is_pated = True
        for elem in figures:
            if self.__update_dots__(elem) != [[], []]:
                is_checkmated = False

        if not self.__king_is_checked__(color):
            return is_pated
        else:
            return False

    # рокировка
    def __long_castling__(self, color):
        king = getattr(self, "king_" + color)
        tara = getattr(self, "tara_" + color + "_1")
        if king.is_walked or tara.is_walked:
            return False
        if color == "white":
            cells = ["B1", "C1", "D1"]
            for elem in cells:
                if elem in self.white_cells or elem in self.black_cells or elem in self.red_cells:
                    return False
            if self.__king_is_checked__(color, "C1") or self.__king_is_checked__(color, "D1"):
                return False

        if color == "black":
            cells = ["G8", "F8", "E8"]
            for elem in cells:
                if elem in self.white_cells or elem in self.black_cells or elem in self.red_cells:
                    return False
            if self.__king_is_checked__(color, "F8") or self.__king_is_checked__(color, "E1"):
                return False

        if color == "red":
            cells = ["M12", "L12", "K12"]
            for elem in cells:
                if elem in self.white_cells or elem in self.black_cells or elem in self.red_cells:
                    return False
            if self.__king_is_checked__(color, "L12") or self.__king_is_checked__(color, "K12"):
                return False

        return True

    def __short_castling__(self, color):
        king = getattr(self, "king_" + color)
        tara = getattr(self, "tara_" + color + "_2")
        if king.is_walked or tara.is_walked:
            return False
        if color == "white":
            cells = ["F1", "G1"]
            for elem in cells:
                if elem in self.white_cells or elem in self.black_cells or elem in self.red_cells:
                    return False
            if self.__king_is_checked__(color, "F1") or self.__king_is_checked__(color, "G1"):
                return False

        if color == "black":
            cells = ["L8", "M8"]
            for elem in cells:
                if elem in self.white_cells or elem in self.black_cells or elem in self.red_cells:
                    return False
            if self.__king_is_checked__(color, "L8") or self.__king_is_checked__(color, "M1"):
                return False

        if color == "red":
            cells = ["B12", "C12"]
            for elem in cells:
                if elem in self.white_cells or elem in self.black_cells or elem in self.red_cells:
                    return False
            if self.__king_is_checked__(color, "B12") or self.__king_is_checked__(color, "C12"):
                return False

        return True
