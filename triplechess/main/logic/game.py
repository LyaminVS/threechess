from .board import Board
from .consts import TURN_CHANGE

class Game:
    def __init__(self):
        self.board = Board()
        self.selected_figure = None
        self.turn = "white"

    def get_dots(self, cell):
        if self.selected_figure and self.selected_figure.letter + self.selected_figure.number == cell:
            self.selected_figure = None
            return [[], [], []]
        for figure in self.board.all_figures:
            if figure.letter + figure.number == cell:
                dots = self.board.__update_dots_2__(figure)
                self.selected_figure = figure
                return dots

    def __transform_to_array__(self):
        array = []
        for elem in self.board.all_figures:
            array.append([elem.type, elem.color, elem.letter + elem.number])
        return array

    def change_position(self, cell):
        if cell in getattr(self.board, self.selected_figure.color+"_cells"):
            if self.selected_figure.color=="white":
                old_cell = "E1"
                if cell=="H1":
                    self.selected_figure.change_cell("G1")
                    self.board.tara_white_2.change_cell("F1")
                    self.board.white_cells.remove("E1")
                    self.board.white_cells.remove("H1")
                    self.board.white_cells.append("G1")
                    self.board.white_cells.append("F1")
                else:
                    self.selected_figure.change_cell("C1")
                    self.board.tara_white_1.change_cell("D1")
                    self.board.white_cells.remove("E1")
                    self.board.white_cells.remove("A1")
                    self.board.white_cells.append("C1")
                    self.board.white_cells.append("D1")
            if self.selected_figure.color=="black":
                old_cell = "K8"
                if cell=="N8":
                    self.selected_figure.change_cell("M8")
                    self.board.tara_black_2.change_cell("L8")
                    self.board.black_cells.remove("K8")
                    self.board.black_cells.remove("N8")
                    self.board.black_cells.append("M8")
                    self.board.black_cells.append("L8")
                else:
                    self.selected_figure.change_cell("F8")
                    self.board.tara_black_1.change_cell("E8")
                    self.board.black_cells.remove("H8")
                    self.board.black_cells.remove("K8")
                    self.board.black_cells.append("F8")
                    self.board.black_cells.append("E8")
            if self.selected_figure.color=="red":
                old_cell = "D12"
                if cell=="A12":
                    self.selected_figure.change_cell("B12")
                    self.board.tara_red_2.change_cell("C12")
                    self.board.red_cells.remove("D12")
                    self.board.red_cells.remove("A12")
                    self.board.red_cells.append("B12")
                    self.board.red_cells.append("C12")
                else:
                    self.selected_figure.change_cell("L12")
                    self.board.tara_red_1.change_cell("K12")
                    self.board.red_cells.remove("D12")
                    self.board.red_cells.remove("N12")
                    self.board.red_cells.append("K12")
                    self.board.red_cells.append("L12")
            color = self.selected_figure.color
            self.selected_figure = None
            figure = "King"

        else:
            if cell in self.board.red_cells:
                self.board.red_cells.remove(cell)
                for figure in self.board.red:
                    if figure.letter + figure.number == cell:
                        self.board.red.remove(figure)
                        self.board.all_figures.remove(figure)
            if cell in self.board.white_cells:
                self.board.white_cells.remove(cell)
                for figure in self.board.white:
                    if figure.letter + figure.number == cell:
                        self.board.white.remove(figure)
                        self.board.all_figures.remove(figure)
            if cell in self.board.black_cells:
                self.board.black_cells.remove(cell)
                for figure in self.board.black:
                    if figure.letter + figure.number == cell:
                        self.board.black.remove(figure)
                        self.board.all_figures.remove(figure)

            old_cell = self.selected_figure.letter + self.selected_figure.number
            self.selected_figure.change_cell(cell)
            figure = self.selected_figure.type
            color = self.selected_figure.color
            self.selected_figure = None
            if old_cell in self.board.white_cells:
                self.board.white_cells.remove(old_cell)
                self.board.white_cells.append(cell)
            if old_cell in self.board.black_cells:
                self.board.black_cells.remove(old_cell)
                self.board.black_cells.append(cell)
            if old_cell in self.board.red_cells:
                self.board.red_cells.remove(old_cell)
                self.board.red_cells.append(cell)

        return old_cell, figure, color

    def reset(self):
        self.board = Board()
        self.turn = "white"
        self.selected_figure = None

    def change_turn(self):
        self.turn = TURN_CHANGE[self.turn]
        return self.turn
