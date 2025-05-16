from utils.util import get_block_index
import math
from utils.Vector3 import Vector3


class Alignment:
    def __init__(self):
        self.startsta = 0.0


class Curve(Alignment):
    def __init__(self):
        super().__init__()
        self.radius = 0.0
        self.cant = 0.0

    def iscurve(self, target_sta: int) -> bool:
        """Check if target_sta falls within this curve segment."""
        return get_block_index(target_sta) == self.startsta and self.radius != 0


class Pitch(Alignment):
    def __init__(self):
        super().__init__()
        self.pitch = 0.0

    def topermilestring(self):
        return f'{self.pitch * 1000:.2f}'

    def isslope(self, target_sta: int) -> bool:
        """Check if target_sta falls within this pitch segment."""
        return get_block_index(target_sta) == self.startsta and self.pitch != 0

    def get_current_pitch_permille(self) -> float:
        return self.pitch * 1000.0

    def todegree(self) -> float:
        """퍼밀 값을 도(degree)로 변환"""
        return math.degrees(math.atan(self.pitch / 1000))  # 퍼밀을 비율로 변환 후 계산


class BVEAlignment:
    """BVEINFO.TXT의 분산된 CURVE, PITCH, COORD통합 선형 클래스
        Attributes:
            startkm (float): 선형 시작 KM
            endkm (float): 선형 끝 KM
            curves(list[Curve]): Curve객체 리스트
            pitchs(list[Pitch]): Pitch객체 리스트
            coords(list[Vector3]): 좌표리스트
        """
    def __init__(self):
        self.startkm: float = 0.0
        self.endkm: float = 0.0
        self.curves: list[Curve] = []
        self.pitchs: list[Pitch] = []
        self.coords: list[Vector3] = []

    def get_curve_at(self, target_sta: int) -> Curve | None:
        for curve in self.curves:
            if curve.iscurve(target_sta):
                return curve
        return None

    def get_pitch_at(self, target_sta: int) -> Pitch | None:
        for pitch in self.pitches:
            if pitch.isslope(target_sta):
                return pitch
        return None

    def get_curve_radius(self, target_sta: int) -> float:
        curve = self.get_curve_at(target_sta)
        return curve.radius if curve else 0.0

    def get_current_curve_string(self, target_sta: int) -> str:
        curve = self.get_curve_at(target_sta)
        return '곡선' if curve else '직선'

    def get_current_pitch_string(self, target_sta: int) -> str:
        pitch = self.get_pitch_at(target_sta)
        return 'slope' if pitch else 'level'

    def get_pitch_permille(self, target_sta: int) -> str:
        pitch = self.get_pitch_at(target_sta)
        return pitch.topermilestring() if pitch else '0.00'
