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

    def count_poles(self) -> int:
        return sum(len(group.poles) for group in self.groups)

    def poles_by_track_for_detail(self) -> dict[int, list[dict]]:
        """
        트랙별 상세 전주 리스트 반환
        { track_index: [ {전주번호, 측점, X, Y, 종류}, ... ] }
        """
        result = {}
        for track in self.track_indices():
            result[track] = [
                {
                    "전주번호": pole.post_number,
                    "측점": pole.pos,
                    "X": pole.coord.x,
                    "Y": pole.coord.y,
                }
                for pole in self.get_poles_by_track(track)
            ]
        return result

    def get_by_id(self, ref_id: int) -> list[PolePlaceDATA] | list:
        lst = []
        for pole in self.iter_poles():
            if pole.ref.id == ref_id:
                lst.extend(pole)

        return lst

    def get_by_id_and_track_idx(
            self, ref_id: int, track_idx: int
    ) -> PolePlaceDATA | None:
        for pole in self.iter_poles():
            if (
                    pole.ref
                    and pole.ref.id == ref_id
                    and pole.track_index == track_idx
            ):
                return pole
        return None

    def get_by_ref(self, ref, track_index):
        return self.get_by_id_and_track_idx(ref.id, track_index)

