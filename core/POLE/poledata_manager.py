from core.POLE.poledata import PoleDATA


class PoleDATAManager:
    """PoleDATA 관리 클래스"""

    def __init__(self):
        self.poles: list[PoleDATA] = []

    def new_pole(self) -> PoleDATA:
        pole = PoleDATA()
        self.poles.append(pole)
        return pole

    def count(self) -> int:
        return len(self.poles)

    def get(self, index: int) -> PoleDATA | None:
        return self.poles[index] if 0 <= index < len(self.poles) else None

    def last(self) -> PoleDATA | None:
        return self.poles[-1] if self.poles else None

    def __iter__(self):
        return iter(self.poles)
