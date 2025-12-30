from core.POLE.polegroup import PoleGroup

class PoleGroupManager:
    """PoleGroup 관리 클래스"""

    def __init__(self):
        self.groups: list[PoleGroup] = []

    def new_group(self, pos: int) -> PoleGroup:
        group = PoleGroup(pos)
        self.groups.append(group)
        return group