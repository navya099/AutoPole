from core.POLE.poledata import PolePlaceDATA


class PoleGroup:
    def __init__(self, pos: int):
        self.pos = pos
        self.poles: dict[int, PolePlaceDATA] = {}

    def get(self, trackidx: int) -> PolePlaceDATA | None:
        return self.poles.get(trackidx)

    def has_track(self, trackidx: int) -> bool:
        return trackidx in self.poles

    def add_pole(self, trackidx: int, pole: PolePlaceDATA):
        if trackidx in self.poles:
            raise ValueError(
                f"Duplicate pole for track {trackidx} at pos {self.pos}"
            )
        self.poles[trackidx] = pole

    def __iter__(self):
        return iter(self.poles.values())

