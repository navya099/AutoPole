
import math
from utils.Vector3 import Vector3


class Alignment:
    """선형 클래스
        Attributes:
            startsta(flaot): 지오메트리 시작측점
    """
    def __init__(self):
        self.startsta = 0.0


class Curve(Alignment):
    """곡선 클래스 Alignment 상속
        Attributes:
            radius(flaot): 곡선반경
            cant(flaot): 캔트
        """
    def __init__(self):
        super().__init__()
        self.radius = 0.0
        self.cant = 0.0

    def iscurve(self, target_sta: int) -> bool:
        """Check if target_sta falls within this curve segment."""
        from utils.util import get_block_index
        return get_block_index(target_sta) == self.startsta and self.radius != 0


class Pitch(Alignment):
    """구배 클래스 Alignment 상속
        Attributes:
            pitch(flaot): 구배
    """
    def __init__(self):
        super().__init__()
        self.pitch = 0.0

    def topermilestring(self):
        """퍼밀로 변환 후 str"""
        return f'{self.pitch * 1000:.2f}'

    def isslope(self, target_sta: int) -> bool:
        """Check if target_sta falls within this pitch segment."""
        from utils.util import get_block_index
        return get_block_index(target_sta) == self.startsta and self.pitch != 0

    def get_current_pitch_permille(self) -> float:
        """pitch를 퍼밀로 변환 float"""
        return self.pitch * 1000.0

    def todegree(self) -> float:
        """퍼밀 값을 도(degree)로 변환"""
        return math.degrees(math.atan(self.pitch / 1000))  # 퍼밀을 비율로 변환 후 계산


class BVEAlignment:
    """BVEINFO.TXT의 분산된 CURVE, PITCH, COORD통합 선형 클래스
        Attributes:
            curves(list[Curve]): Curve객체 리스트
            pitchs(list[Pitch]): Pitch객체 리스트
            coords(list[Vector3]): 좌표리스트
        """

    def __init__(self):
        self.curves: list[Curve] = []
        self.pitchs: list[Pitch] = []
        self.coords: list[Vector3] = []

    def get_curve_at(self, target_sta: int) -> Curve | None:
        """타겟 측점의 곡선 객체 반환"""
        for curve in self.curves:
            if curve.iscurve(target_sta):
                return curve
        return None

    def get_pitch_at(self, target_sta: int) -> Pitch | None:
        """타겟 측점의 구배 객체 반환"""
        for pitch in self.pitchs:
            if pitch.isslope(target_sta):
                return pitch
        return None

    def get_coord_at_index(self, index: int) -> Vector3 | None:
        """현재 인덱스의 좌표 객체 반환"""
        if 0 <= index < len(self.coords):
            return self.coords[index]
        return None

    def get_coord_at_station(self, target_sta: int) -> Vector3:
        """타겟 측점의 좌표객체 반환"""
        index = self.get_index(target_sta)
        coord = self.get_coord_at_index(index)
        return coord

    def get_curve_radius(self, target_sta: int) -> float:
        """타겟 측점의 곡선반경 반환"""
        curve = self.get_curve_at(target_sta)
        return curve.radius if curve else 0.0

    def get_current_curve_string(self, target_sta: int) -> str:
        """타겟 측점의 곡선|직선을 반환"""
        curve = self.get_curve_at(target_sta)
        return '곡선' if curve else '직선'

    def get_current_pitch_string(self, target_sta: int) -> str:
        """타겟 측점의 수평|경사 반환"""
        pitch = self.get_pitch_at(target_sta)
        return 'slope' if pitch else 'level'

    def get_pitch_permille(self, target_sta: int) -> str:
        """타겟 측점의 구배 반환(str)"""
        pitch = self.get_pitch_at(target_sta)
        return pitch.topermilestring() if pitch else '0.00'

    def get_curve_cant(self, target_sta: int) -> float:
        """타겟 측점의 캔트 반환"""
        curve = self.get_curve_at(target_sta)
        return curve.cant if curve else 0.0

    def get_index(self, target_sta: float) -> int:
        start = self.curves[0].startsta  # 실제 데이터의 시작 station
        step = self.curves[1].startsta - self.curves[0].startsta  # 샘플링 간격 (보통 25m)

        offset = target_sta - start
        index = int(offset // step)
        return index

    def get_station_at_index(self, index: int) -> float:
        """인덱스에 해당하는 측점 반환"""
        return self.curves[index].startsta

    @property
    def startkm(self) -> float:
        """startkm (float): 선형 시작 KM"""
        return self.curves[0].startsta if self.curves else 0.0

    @property
    def endkm(self) -> float:
        """endkm (float): 선형 끝 KM"""
        return self.curves[-1].startsta if self.curves else 0.0

