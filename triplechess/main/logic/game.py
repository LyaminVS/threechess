from .board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.selected_figure = None

    def get_dots(self, cell):
        for figure in self.board.all_figures:
            if figure.letter + figure.number == cell:
                dots = self.board.__update_dots__(figure)

                self.selected_figure = figure
                return dots

    def __transform_to_array__(self):
        array = []
        for elem in self.board.all_figures:
            array.append([elem.type, elem.color, elem.letter + elem.number])
        return array

    def change_position(self, cell):
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
