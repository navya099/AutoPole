from core.POLE.pole_utils import PoleUtils
from core.POLE.poledata import PolePlaceDATA
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

    def update_post_numbers(self):
        positions = [group.pos for group in self.groups]

        post_number_map = PoleUtils.generate_postnumbers(positions)

        for group in self.groups:
            post_number = post_number_map.get(group.pos)
            if not post_number:
                continue

            for pole in group:
                pole.post_number = post_number

    def track_indices(self) -> list[int]:
        indices = set()
        for group in self.groups:
            indices.update(group.poles.keys())
        return sorted(indices)

    def get_poles_by_track(self, trackidx: int) -> list[PolePlaceDATA]:
        poles = []
        for group in sorted(self.groups, key=lambda g: g.pos):
            pole = group.get(trackidx)
            if pole:
                poles.append(pole)
        return poles

    def sorted_groups(self):
        return sorted(self.groups, key=lambda g: g.pos)