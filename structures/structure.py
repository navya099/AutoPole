from dataclasses import dataclass
from utils.logger import logger

"""
StructureFactory 클래스로 구조물 생성추상화
"""


@dataclass
class Structure:
    """구조물 공통 기능을 관리하는 부모 클래스
            Attributes:
                name (str): 구조물 명칭
                structuretype (str): 구조물 종류(교량/터널)
                startsta(float): 시작 측점 m
                endsta(float): 끝 측점 m
            """
    name: str
    structuretype: str
    startsta: float
    endsta: float

    @property
    def length(self) -> float:
        """구조물 길이 length(endsta - startsta)"""
        return self.endsta - self.startsta

    def isstructure(self, targetsta: float) -> bool:
        """targetsta가 구조물 범위 내에 있는지 확인"""
        return self.startsta <= targetsta <= self.endsta

    def contains(self, targetsta: float) -> bool:
        """get_structure_type_if_contains호출을 위한 래퍼 메서드"""
        return self.isstructure(targetsta)

    def get_structure_type_if_contains(self, targetsta: float) -> str | None:
        """targetsta가 구조물 범위 내에 있는지 확인 후 타입 리턴"""
        if self.contains(targetsta):
            return self.structuretype
        return None

    def get_structure_stas(self) -> tuple[float, float]:
        """구조물의 시작 측점과 끝 측점 반환"""
        return self.startsta, self.endsta


class Bridge(Structure):
    """교량 클래스 (Structure상속)
    """

    def __init__(self, name: str, startsta: float, endsta: float):
        super().__init__(name, '교량', startsta, endsta)


class Tunnel(Structure):
    """터널 클래스 (Structure상속)
    """

    def __init__(self, name: str, startsta: float, endsta: float):
        super().__init__(name, '터널', startsta, endsta)


class StructureCollection(list):
    """구조물들을 컬렉션하는 클래스(리스트 상속)"""

    def __init__(self):
        super().__init__()

    def get_by_type(self, structuretype: str) -> list[Structure]:
        """구조물을 타입별로 얻기"""
        return [s for s in self if s.structuretype == structuretype]

    def find_containing(self, targetsta: float) -> Structure | None:
        """targetsta가 포함된 첫 번째 구조물을 반환"""
        for s in self:
            if s.isstructure(targetsta):
                return s
        return None  # 없을 경우 None 반환

    def all_structures(self) -> list[Structure]:
        """모든 구조물 리스트 반환"""
        return list(self)  # self 자체가 리스트이므로 그대로 반환

    def get_structure_type_at(self, sta: float) -> str:
        """
        주어진 위치 sta가 교량, 터널, 토공인지 판별하는 메서드.

        :param sta: 위치 (거리값)
        :return: '교량', '터널', 또는 '토공'
        """
        try:
            structure = self.find_containing(sta)
            if structure:
                return structure.structuretype

        except Exception as ex:
            logger.error(
                f"structure lookup failed: {type(ex).__name__} - {ex} | sta={sta}")
        return '토공'

    def apply_offset(self, offset: float = 0.0):
        """
        모든 구조물의 시작/끝 측점에 동일한 offset을 적용.
        예: offset=100 → 모든 startsta, endsta에 +100
        """
        for s in self:
            s.startsta += offset
            s.endsta += offset

class StructureFactory:
    """구조물 객체를 생성하는 팩토리 클래스"""
    registry = {
        '교량': Bridge,
        '터널': Tunnel,
    }

    @classmethod
    def create_structure(cls, structuretype: str, name: str, startsta: float, endsta: float) -> Structure:
        """구조물 생성 팩토리메서드"""
        if structuretype not in cls.registry:
            raise ValueError(f"지원하지 않는 구조물 타입입니다: {structuretype}")
        return cls.registry[structuretype](name, startsta, endsta)
