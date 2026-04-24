from .figure import *
from .consts import f, TURN_CHANGE


class Peshka(Figure):
    def __init__(self, cell, color, on_road=False):
        super(Peshka, self).__init__(cell, color)
        self.__div_cells__()
        self.__first_n_zero_cells__()
        self.type = "Peshka"

    def __first_n_zero_cells__(self):
        self.first_red = []
        self.first_black = []
        self.first_white = []
        self.zero_red = []
        self.zero_black = []
        self.zero_white = []
        for let in LETTERS_1 + LETTERS_3:
            self.first_red.append(let + "11")
        for let in LETTERS_2 + LETTERS_3:
            self.first_black.append(let + "7")
        for let in LETTERS_1 + LETTERS_2:
            self.first_white.append(let + "2")
        for let in LETTERS_1 + LETTERS_3:
            self.zero_red.append(let + "12")
        for let in LETTERS_2 + LETTERS_3:
            self.zero_black.append(let + "8")
        for let in LETTERS_1 + LETTERS_2:
            self.zero_white.append(let + "1")

    @staticmethod
    def double_step_skipped_cell(pawn_color, old_str, new_str, white, black, red, grey):
        p = Peshka(old_str, pawn_color)
        all_occ = list(white) + list(black) + list(red) + list(grey)
        c = p.cell
        if pawn_color == "white":
            if c.cell[0] in p.first_white and c.top[0] not in all_occ:
                t1 = c.top[0]
                t2n = f(t1).top[0] if f(t1).top else None
                if t2n == new_str:
                    return t1
            return None
        if pawn_color == "black":
            if c.cell[0] in p.red:
                return None
            if c.cell[0] in p.first_black and c.bottom[0] not in all_occ:
                t1 = c.bottom[0]
                t2n = f(t1).bottom[0] if f(t1).bottom else None
                if t2n == new_str:
                    return t1
            return None
        if pawn_color == "red":
            if c.cell[0] in p.black:
                return None
            if c.cell[0] in p.first_red and c.bottom[0] not in all_occ:
                t1 = c.bottom[0]
                t2n = f(t1).bottom[0] if f(t1).bottom else None
                if t2n == new_str:
                    return t1
            return None
        return None

    def _peshka_forward_left_right(self):
        if self.color == "white":
            return "left_top", "right_top"
        if self.color == "black":
            if self.cell.cell[0] in self.red:
                return "left_top", "right_top"
            return "left_bottom", "right_bottom"
        if self.color == "red":
            if self.cell.cell[0] in self.black:
                return "left_top", "right_top"
            return "left_bottom", "right_bottom"
        return "left_top", "right_top"

    def _diagonal_capture_cell_names(self):
        la, ra = self._peshka_forward_left_right()
        out = []
        for c in getattr(self.cell, la, []) or []:
            if c:
                out.append(c)
        for c in getattr(self.cell, ra, []) or []:
            if c:
                out.append(c)
        return out

    def __div_cells__(self):
        self.red = []
        self.black = []
        self.white = []
        for let in LETTERS_1 + LETTERS_3:
            for n in NUMBERS_3:
                self.red.append(let + n)
        for let in LETTERS_2 + LETTERS_3:
            for n in NUMBERS_2:
                self.black.append(let + n)
        for let in LETTERS_1 + LETTERS_2:
            for n in NUMBERS_1:
                self.white.append(let + n)

    def __check_3_cells__(self, forward, forward_left, forward_right, white, black, red, grey):
        dots = []
        dots_eat = []
        dots_eat_temp, dots_temp, dots_save_temp = self.__check__(getattr(self.cell, forward)[0], white, black, red,
                                                                  grey)
        dots += dots_temp
        for c in getattr(self.cell, forward_left):
            dots_eat_temp, dots_temp, dots_save_temp = self.__check__(c, white, black, red, grey)
            dots_eat += dots_eat_temp
        for c in getattr(self.cell, forward_right):
            dots_eat_temp, dots_temp, dots_save_temp = self.__check__(c, white, black, red, grey)
            dots_eat += dots_eat_temp
        return dots, dots_eat

    def __dots__(self, white, black, red, grey, en_passant=None):
        dots_eat = []
        dots = []
        dots_replace = []
        if self.color == "white":
            dots_temp, dots_eat_temp = self.__check_3_cells__("top", "left_top", "right_top", white, black, red, grey)
            dots += dots_temp
            dots_eat += dots_eat_temp
            if self.cell.cell[0] in self.first_white and not(self.cell.top[0] in white or self.cell.top[0] in black or self.cell.top[0] in red or self.cell.top[0] in grey):
                dots_eat_temp, dots_temp, dots_save_temp = self.__check__(f(self.cell.top[0]).top[0], white, black, red,
                                                                          grey)
                dots += dots_temp
            if self.cell.cell[0] in self.zero_black or self.cell.cell[0] in self.zero_red:
                dots_replace.append(self.cell.cell[0])
                self.on_road = True
        if self.color == "black":
            if self.cell.cell[0] in self.zero_white or self.cell.cell[0] in self.zero_red:
                dots_replace.append(self.cell.cell[0])
                self.on_road = True
            if self.cell.cell[0] in self.red:

                dots_temp, dots_eat_temp = self.__check_3_cells__("top", "left_top", "right_top", white, black, red,
                                                                  grey)
                dots += dots_temp
                dots_eat += dots_eat_temp
            else:

                dots_temp, dots_eat_temp = self.__check_3_cells__("bottom", "left_bottom", "right_bottom", white, black,
                                                                  red, grey)
                dots += dots_temp
                dots_eat += dots_eat_temp
                if self.cell.cell[0] in self.first_black and not(self.cell.bottom[0] in white or self.cell.bottom[0] in black or self.cell.bottom[0] in red or self.cell.bottom[0] in grey):
                    dots_eat_temp, dots_temp, dots_save_temp = self.__check__(f(self.cell.bottom[0]).bottom[0], white,
                                                                              black,
                                                                              red, grey)
                    dots += dots_temp
        if self.color == "red":
            if self.cell.cell[0] in self.zero_black or self.cell.cell[0] in self.zero_white:
                dots_replace.append(self.cell.cell[0])
                self.on_road = True
            if self.cell.cell[0] in self.black:
                dots_temp, dots_eat_temp = self.__check_3_cells__("top", "left_top", "right_top", white, black, red,
                                                                  grey)
                dots += dots_temp
                dots_eat += dots_eat_temp
            else:
                dots_temp, dots_eat_temp = self.__check_3_cells__("bottom", "left_bottom", "right_bottom", white, black,
                                                                  red, grey)
                dots += dots_temp
                dots_eat += dots_eat_temp
                if self.cell.cell[0] in self.first_red and not(self.cell.bottom[0] in white or self.cell.bottom[0] in black or self.cell.bottom[0] in red or self.cell.bottom[0] in grey):
                    dots_eat_temp, dots_temp, dots_save_temp = self.__check__(f(self.cell.bottom[0]).bottom[0], white,
                                                                              black,
                                                                              red, grey)
                    dots += dots_temp
        if en_passant and en_passant.get("victim") and en_passant.get("skipped") and en_passant.get("pusher") is not None:
            pusher = en_passant["pusher"]
            pusher_list = white if pusher == "white" else black if pusher == "black" else red
            vcell = en_passant["victim"]
            st = en_passant.get("stage", 0)
            r1, r2 = TURN_CHANGE[pusher], TURN_CHANGE[TURN_CHANGE[pusher]]
            active = r1 if st == 0 else r2
            if (self.type == "Peshka" and self.color != pusher and self.color == active
                    and vcell in pusher_list and en_passant["skipped"] in self._diagonal_capture_cell_names()
                    and en_passant["skipped"] not in dots_eat):
                dots_eat.append(en_passant["skipped"])
        return dots, dots_eat, dots_replace
