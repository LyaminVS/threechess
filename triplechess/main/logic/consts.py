# import board_rules
from .board_rules import BoardRules

LETTERS_1 = ['A', 'B', 'C', 'D']
LETTERS_2 = ['E', 'F', 'G', 'H']
LETTERS_3 = ['K', 'L', 'M', 'N']
NUMBERS_1 = ['1', '2', '3', '4']
NUMBERS_2 = ['5', '6', '7', '8']
NUMBERS_3 = ['9', '10', '11', '12']

TURN_DIR = {
    "right_bottom": "left_top",
    "left_top": "right_bottom",
    "right_top": "left_bottom",
    "left_bottom": "right_top",
    "top": "bottom",
    "bottom": "top",
    "left": "right",
    "right": "left",
}
# 1 - 13
# 2 - 12
# 3 - 23

BOARD_RULES = BoardRules()


def f(string):
    return getattr(BOARD_RULES, string)
