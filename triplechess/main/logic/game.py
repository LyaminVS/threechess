import jsonpickle
from .board import Board
from .consts import TURN_CHANGE
from .tara import Tara as Tara
from .officer import Officer as Officer
from .peshka import Peshka as Peshka
from .queen import Queen as Queen
from .king import King as King
from .horse import Horse as Horse

class Game:
    def __init__(self):
        self.board = Board()
        self.selected_figures = {
            "white": None,
            "black": None,
            "red": None,
        }
        self.turn = "white"
        self.en_passant = None

    def _sync_en_passant_to_board(self):
        self.board.en_passant = self.en_passant

    def _remove_figure_on_cell(self, target_cell):
        for name, lst in (("red", self.board.red), ("white", self.board.white), ("black", self.board.black)):
            if target_cell in getattr(self.board, name + "_cells"):
                getattr(self.board, name + "_cells").remove(target_cell)
                for fig in list(lst):
                    if fig.letter + fig.number == target_cell:
                        lst.remove(fig)
                        self.board.all_figures.remove(fig)
                        break
                return

    def _en_passant_legal(self, color, ep):
        pusher = ep["pusher"]
        r1, r2 = TURN_CHANGE[pusher], TURN_CHANGE[TURN_CHANGE[pusher]]
        active = r1 if ep.get("stage", 0) == 0 else r2
        if color != active:
            return False
        for fig in self.board.all_figures:
            if fig.cell_str == ep["victim"] and fig.color == pusher and fig.type == "Peshka":
                return True
        return False

    def _update_en_passant_after_move(self, old_cell, new_cell, color, moving_type, was_ep=False):
        if was_ep:
            self._sync_en_passant_to_board()
            return
        w, b, r, g = self.board.white_cells, self.board.black_cells, self.board.red_cells, self.board.grey_cells
        if moving_type == "Peshka":
            sk = Peshka.double_step_skipped_cell(color, old_cell, new_cell, w, b, r, g)
            if sk:
                for fig in self.board.all_figures:
                    if fig.cell_str == new_cell and fig.type == "Peshka" and fig.color == color:
                        self.en_passant = {
                            "victim": new_cell,
                            "skipped": sk,
                            "pusher": color,
                            "stage": 0,
                        }
                        self._sync_en_passant_to_board()
                        return
        if not self.en_passant:
            self._sync_en_passant_to_board()
            return
        ep = self.en_passant
        pusher = ep.get("pusher")
        victim = ep.get("victim")
        pusher_list = w if pusher == "white" else b if pusher == "black" else r
        if not victim or victim not in pusher_list:
            self.en_passant = None
            self._sync_en_passant_to_board()
            return
        ok = False
        for fig in self.board.all_figures:
            if fig.cell_str == victim and fig.color == pusher and fig.type == "Peshka":
                ok = True
                break
        if not ok:
            self.en_passant = None
            self._sync_en_passant_to_board()
            return
        if old_cell == victim and color == pusher:
            self.en_passant = None
            self._sync_en_passant_to_board()
            return
        if new_cell == victim:
            self.en_passant = None
            self._sync_en_passant_to_board()
            return
        r1, r2 = TURN_CHANGE[pusher], TURN_CHANGE[TURN_CHANGE[pusher]]
        active = r1 if ep.get("stage", 0) == 0 else r2
        if color == active:
            if ep.get("stage", 0) == 0:
                self.en_passant = {**ep, "stage": 1}
            else:
                self.en_passant = None
        self._sync_en_passant_to_board()

    def get_dots(self, cell, color, ignore_duplication):
        self._sync_en_passant_to_board()
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
        self._sync_en_passant_to_board()
        old_cell = self.selected_figures[color].letter + self.selected_figures[color].number
        if cell in getattr(self.board, color + "_cells"):
            if color == "white":
                old_cell = "E1"
                king_new = "G1" if cell == "H1" else "C1"
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
                king_new = "M8" if cell == "N8" else "F8"
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
                king_new = "B12" if cell == "A12" else "L12"
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
            self._update_en_passant_after_move(old_cell, king_new, color, "King", was_ep=False)
        else:
            moving = self.selected_figures[color]
            moving_type = moving.type
            ep = self.en_passant
            is_ep = (
                ep
                and moving_type == "Peshka"
                and cell == ep.get("skipped")
            )
            if is_ep and self._en_passant_legal(color, ep):
                victim = ep["victim"]
                self._remove_figure_on_cell(victim)
                moving.change_cell(cell)
                self.en_passant = None
                self._sync_en_passant_to_board()
                figure = "Peshka"
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
                self.__is_peshka_go_through__()
                self._update_en_passant_after_move(old_cell, cell, color, moving_type, was_ep=True)
                return old_cell, figure, color
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

            self.__is_peshka_go_through__()
            self._update_en_passant_after_move(old_cell, cell, color, moving_type, was_ep=False)

        return old_cell, figure, color

    def reset(self):
        self.board = Board()
        self.turn = "white"
        self.en_passant = None
        self.selected_figures["white"] = self.selected_figures["black"] = self.selected_figures["red"] = None

    def change_turn(self):
        self.turn = TURN_CHANGE[self.turn]
        return self.turn

    def clear_board_for_setup(self):
        self.board.white = []
        self.board.black = []
        self.board.red = []
        self.board.white_cells = []
        self.board.black_cells = []
        self.board.red_cells = []
        self.board.grey = []
        self.board.grey_cells = []
        self.board.all_figures = []
        self.selected_figures["white"] = None
        self.selected_figures["black"] = None
        self.selected_figures["red"] = None
        self.turn = "white"
        self.en_passant = None

    def place_figure_for_setup(self, cell, figure_type, color):
        cls_map = {
            "King": King,
            "Queen": Queen,
            "Tara": Tara,
            "Officer": Officer,
            "Horse": Horse,
            "Peshka": Peshka,
        }
        if color not in ("white", "black", "red"):
            return False
        figure_cls = cls_map.get(figure_type)
        if figure_cls is None:
            return False
        self.remove_figure_for_setup(cell)
        figure = figure_cls(cell, color)
        getattr(self.board, color).append(figure)
        getattr(self.board, color + "_cells").append(cell)
        self.board.all_figures.append(figure)
        return True

    def remove_figure_for_setup(self, cell):
        for color in ("white", "black", "red"):
            cells = getattr(self.board, color + "_cells")
            if cell in cells:
                cells.remove(cell)
            figures = getattr(self.board, color)
            for idx, figure in enumerate(list(figures)):
                if figure.cell_str == cell:
                    del figures[idx]
                    break
        for idx, figure in enumerate(list(self.board.all_figures)):
            if figure.cell_str == cell:
                del self.board.all_figures[idx]
                break
        for c in ("white", "black", "red"):
            sf = self.selected_figures.get(c)
            if sf and sf.cell_str == cell:
                self.selected_figures[c] = None
        return True

    def __is_peshka_go_through__(self):

        colors = ["white", "black", "red"]
        cells = [["12", "8"], ["1", "12"], ["1", "8"]]
        for i in range(3):
            for j in range(1, 9):
                peshka = getattr(self.board, "peshka_" + colors[i] + "_" + str(j))
                if peshka.number in cells[i] and peshka.type=="Peshka":
                    self.__transform_peshka__(peshka.cell_str, "Horse") #Пешки превращаются в лошадей
                    return peshka.cell_str

        return ""

    def __transform_peshka__(self, cell, type):
        for i in range(len(self.board.all_figures)):
            if self.board.all_figures[i].cell_str == cell:
                peshka_color = self.board.all_figures[i].color
                new_figure = None

                if type=="Queen":
                    new_figure = Queen(cell, peshka_color)
                if type=="Tara":
                    new_figure = Tara(cell, peshka_color)
                if type=="Horse":
                    new_figure = Horse(cell, peshka_color)
                if type=="Officer":
                    new_figure = Officer(cell, peshka_color)

                self.board.all_figures[i] = new_figure
                self.board.all_figures[i].is_walked = True
                for j in range(1,9):
                    if getattr(self.board, "peshka_"+peshka_color+"_"+str(j)).cell_str == cell:
                        setattr(self.board, "peshka_"+peshka_color+"_"+str(j), new_figure)
                        for k in range(16):
                            if getattr(self.board, peshka_color)[k].cell_str == cell:
                                getattr(self.board, peshka_color)[k] = new_figure
                            break
                        break
                break


    def game_to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def json_to_game(cls, json):
        return jsonpickle.decode(json)

    def is_color_right(self, color):
        return self.turn == color

    def is_turn_legal(self, cell, color):
        self._sync_en_passant_to_board()
        selected_figure = self.selected_figures[color]
        dots = self.board.__update_dots_2__(selected_figure)
        return any(cell in dots[i] for i in range(len(dots)))