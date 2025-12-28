from core.POLE.poledata import PoleDATA
from core.POLE.polegroup import PoleGroup


class PoleDATAManager:
    """PoleDATA 관리 클래스"""

    def __init__(self):
        self.groups: list[PoleGroup] = []

    def new_group(self, pos: int) -> PoleGroup:
        group = PoleGroup(pos)
        self.groups.append(group)
        return group

    def count(self) -> int:
        return len(self.poles)

    def get(self, index: int) -> PoleDATA | None:
        return self.poles[index] if 0 <= index < len(self.poles) else None

    def last(self) -> PoleDATA | None:
        return self.poles[-1] if self.poles else None

    def __iter__(self):
        return iter(self.poles)

    @property
    def poles(self) -> list[PoleDATA]:
        """기존 Manager들과 호환용"""
        return [p for g in self.groups for p in g.poles]
