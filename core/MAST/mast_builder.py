from core.POLE.poledata import PolePlaceDATA
from core.section.section_rules import SectionRule
from utils.util import Direction
import math

class MastBuilder:
    def build(self, ref, track_idx, base_direction, policy, speed):
        pole = PolePlaceDATA()

        # 기본 속성
        pole.track_index = track_idx
        pole.pos = ref.pos
        pole.span = ref.span
        pole.direction = (
            base_direction
            if track_idx == 0
            else Direction.opposite(base_direction)
        )
        pole.coord = ref.center_coord

        #전주고유속성계산
        pole.gauge = SectionRule.get_gauge(ref.structure_type)#건식게이지
        isleft = (pole.direction == Direction.LEFT)
        theta = ref.azimuth
        azimuth = theta + math.pi / 2 if isleft else theta - math.pi / 2

        #실제좌표계산
        pole.coord.move(azimuth, pole.gauge)

        # Mast 결정
        specs = policy.decide(ref, pole, speed)
        pole.apply_mast(specs)

        return pole
