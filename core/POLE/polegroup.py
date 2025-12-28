from core.POLE.poledata import PoleDATA


class PoleGroup:
    def __init__(self, pos: int):
        self.pos = pos
        self.poles: list[PoleDATA] = []

    def add_pole(self, pole: PoleDATA):
        self.poles.append(pole)
