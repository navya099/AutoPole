from dataclasses import dataclass

from core.AIRJOINT.airjoint_state import AirJointState
from utils.util import Direction


@dataclass
class BracketSpec:
    """브래킷 프로토콜용 데이터클래스
    Attributes:
        bracket_type: # inner / outer
        install_type: # OpG / Tn
        gauge: 건식게이지
        name: 브래킷 풀네임
        index: 브래킷 인덱스
        airjoint: 에어조인트 상태
    """    # I / O
    bracket_type: str      # inner / outer
    install_type: str      # OpG / Tn
    gauge: float
    direction: Direction
    name: str
    index: int
    airjoint: AirJointState | None = None


