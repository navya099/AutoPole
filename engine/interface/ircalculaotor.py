from core.POLE.pole_refdata import PoleRefData
from core.POLE.poledata import PolePlaceDATA
from point3d import Point3d
import math
from utils.util import Direction

class IRCalculator:
    def calc_offset_position(self, pole: PolePlaceDATA, offset: float) -> Point3d:
        """원점에서 offset만큼 떨어진 좌표 반환"""
        azimuth = pole.ref.azimuth
        azimuth_tangent = azimuth + math.pi/ 2 if pole.direction == Direction.LEFT else azimuth - math.pi / 2
        coord = pole.coord.copy()
        coord.move(azimuth_tangent, offset)
        return coord

    def calc_offset_position_xy(self, pole: PolePlaceDATA, offset_x: float, offset_y: float) -> Point3d:
        """원점에서 x,y만큼 떨어진 좌표 반환"""
        azimuth = pole.ref.azimuth
        azimuth_tangent = azimuth + math.pi / 2 if pole.direction == Direction.LEFT else azimuth - math.pi / 2
        coord = pole.coord.copy()
        coord.move(azimuth_tangent, offset_x)
        coord.z += offset_y
        return coord