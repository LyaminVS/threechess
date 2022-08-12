import jsonpickle
from .board import Board
from .consts import TURN_CHANGE


class Game:
    def __init__(self):
        self.board = Board()
        self.selected_figures = {
            "white": None,
            "black": None,
            "red": None,
        }
        self.turn = "white"

    def get_dots(self, cell, color, ignore_duplication):
        if self.selected_figures[color] and self.selected_figures[color].cell_str == cell and not ignore_duplication:
            self.selected_figures[color] = None
            return [[], [], []]
        for figure in self.board.all_figures:
            if figure.letter + figure.number == cell:
                dots = self.board.__update_dots_2__(figure)
                self.selected_figures[color] = figure
                return dots

    def __transform_to_array__(self):
        array = []
        for elem in self.board.all_figures:
            array.append([elem.type, elem.color, elem.letter + elem.number])
        return array

    def change_position(self, cell, color):
        old_cell = self.selected_figures[color].letter + self.selected_figures[color].number
        if cell in getattr(self.board, color + "_cells"):
            if color == "white":
                old_cell = "E1"
                if cell == "H1":
                    self.selected_figures[color].change_cell("G1")
                    self.board.tara_white_2.change_cell("F1")
                    self.board.white_cells.remove("E1")
                    self.board.white_cells.remove("H1")
                    self.board.white_cells.append("G1")
                    self.board.white_cells.append("F1")
                else:
                    self.selected_figures[color].change_cell("C1")
                    self.board.tara_white_1.change_cell("D1")
                    self.board.white_cells.remove("E1")
                    self.board.white_cells.remove("A1")
                    self.board.white_cells.append("C1")
                    self.board.white_cells.append("D1")
            if color == "black":
                old_cell = "K8"
                if cell == "N8":
                    self.selected_figures[color].change_cell("M8")
                    self.board.tara_black_2.change_cell("L8")
                    self.board.black_cells.remove("K8")
                    self.board.black_cells.remove("N8")
                    self.board.black_cells.append("M8")
                    self.board.black_cells.append("L8")
                else:
                    self.selected_figures[color].change_cell("F8")
                    self.board.tara_black_1.change_cell("E8")
                    self.board.black_cells.remove("H8")
                    self.board.black_cells.remove("K8")
                    self.board.black_cells.append("F8")
                    self.board.black_cells.append("E8")
            if color == "red":
                old_cell = "D12"
                if cell == "A12":
                    self.selected_figures[color].change_cell("B12")
                    self.board.tara_red_2.change_cell("C12")
                    self.board.red_cells.remove("D12")
                    self.board.red_cells.remove("A12")
                    self.board.red_cells.append("B12")
                    self.board.red_cells.append("C12")
                else:
                    self.selected_figures[color].change_cell("L12")
                    self.board.tara_red_1.change_cell("K12")
                    self.board.red_cells.remove("D12")
                    self.board.red_cells.remove("N12")
                    self.board.red_cells.append("K12")
                    self.board.red_cells.append("L12")
            self.selected_figures[color] = None
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

            self.selected_figures[color].change_cell(cell)
            figure = self.selected_figures[color].type
            self.selected_figures[color] = None
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
        self.selected_figures["white"] = self.selected_figures["black"] = self.selected_figures["red"] = None

    def change_turn(self):
        self.turn = TURN_CHANGE[self.turn]
        return self.turn

    def __is_peshka_go_through__(self):
        colors = ["white", "black", "red"]
        cells = [["12", "8"], ["1", "12"], ["1", "8"]]
        for i in range(3):
            for j in range(1, 9):
                peshka = getattr(self.board, "peshka_" + colors[i] + "_" + str(j))
                if peshka.number in cells[i]:
                    return peshka.cell_str

        return ""

    # def __transform_peshka__(self, cell, type):
    #     for i in range(len(self.board.all_figures)):
    #         if self.board.all_figures[i].cell_str == cell:
    #             if type=="Queen":
    #                 queen = Queen(cell,"white")
    #                 self.board.all_figures[i] = queen
    #                 self.board.peshka_white_1 = queen
    #                 self.board.white.append(queen)
    #             if type=="Tara":
    #                 self.board.all_figures[i] = Tara(cell,self.board.all_figures[i].color)
    #             if type=="Horse":
    #                 self.board.all_figures[i] = Horse(cell,self.board.all_figures[i].color)
    #             if type=="Officer":
    #                 self.board.all_figures[i] = Officer(cell,self.board.all_figures[i].color)
    #             self.board.all_figures[i].is_walked = True
    #             break
    #

    def game_to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def json_to_game(cls, json):
        return jsonpickle.decode(json)
