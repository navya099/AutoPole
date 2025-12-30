from core.POLE.polegroup import PoleGroup

class PoleGroupCollection:
    """PoleGroup 관리 클래스"""

    def __init__(self):
        self.groups: list[PoleGroup] = []

    def new_group(self, pos: int) -> PoleGroup:
        group = PoleGroup(pos)
        self.groups.append(group)
        return group

    def __iter__(self):
        return iter(self.groups)

    def iter_poles(self):
        for group in self:
            yield from group
