from core.POLE.pole_refdata import PoleRefData
from core.POLE.poledata import PolePlaceDATA
from core.POLE.polegroup_collector import PoleGroupCollection
from core.POLE.poleplace_builder import PolePlaceBuilder
from utils.util import Direction

def make_pole(
    pos: float,
    span: float,
    gauge: float = 3.0,
    direction: Direction = Direction.LEFT,
):
    pole = PolePlaceDATA()
    pole.pos = pos
    pole.span = span
    pole.gauge = gauge
    pole.direction = direction

    return pole

def make_ref(pos, span, gauge, direction):
    ref = PoleRefData()
    ref.pos = pos
    ref.span = span
    ref.gauge = gauge
    ref.direction = direction

    return ref

class PoleTESTFctory:
    def run(self, track_count, number_pole):
        builder = PolePlaceBuilder()
        self.collection = PoleGroupCollection()
        polerefs = [make_ref(pos=i * 50, span=50, gauge=3, direction=Direction.LEFT) for i in range(number_pole + 1)]
        for ref in polerefs:
            group = self.collection.new_group(ref.pos)
            for track_idx in range(track_count):
                try:
                    if track_idx == 0:
                        direction = Direction.LEFT
                    else:
                        direction = Direction.RIGHT
                    pole = make_pole(pos=ref.pos,span=50,gauge=3.0,direction=direction)
                    pole.ref = ref
                    group.add_pole(track_idx, pole)
                except Exception:
                        print(f"Pole 생성 실패 (pos={ref}, track={track_idx})")