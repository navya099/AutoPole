from core.POLE.poledata import PolePlaceDATA
from core.section.section_rules import SectionRule
from utils.util import Direction
import math

class PolePlaceBuilder:
    def build(self, ref, track_idx, base_direction) -> PolePlaceDATA:
        pole = PolePlaceDATA()
        pole.track_index = track_idx
        pole.pos = ref.pos
        pole.span = ref.span
        pole.ref = ref
        pole.current_section =ref.section_info
        pole.direction = (
            base_direction
            if track_idx == 0
            else Direction.opposite(base_direction)
        )

        pole.coord = ref.center_coord.copy()
        pole.gauge = SectionRule.get_gauge(ref.structure_type)

        isleft = (pole.direction == Direction.LEFT)

        azimuth = ref.azimuth + math.pi / 2 if isleft else ref.azimuth - math.pi / 2
        pole.coord.move(azimuth, pole.gauge)

        return pole
