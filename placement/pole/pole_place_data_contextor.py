from core.POLE.pole_refdata import PoleRefData
from core.POLE.poledata import PolePlaceDATA


class PolePlacementContext:
    def __init__(self):
        self._map: dict[int, PolePlaceDATA] = {}

    def register(self, pole: PolePlaceDATA):
        self._map[pole.ref.id] = pole

    def get(self, ref: PoleRefData) -> PolePlaceDATA:
        try:
            return self._map[ref.id]
        except KeyError:
            raise KeyError(f"Pole not placed: {ref.id}")
