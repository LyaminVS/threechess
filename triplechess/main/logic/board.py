import tara

class Board:
    def __init__(self):
        self.white = []
        tara1 = tara("A", 1)
        tara2 = tara("H", 1)
        self.white += tara1 + tara2
