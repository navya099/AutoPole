from enum import Enum, auto

class SectionType(Enum):
    NORMAL = auto()           # 일반개소
    AIRJOINT = auto()         # 에어조인트
    AIRSECTION = auto()       # 에어섹션
    NEUTRALSECTION = auto()   # 절연구간
    STATION = auto()          # 정거장
