from dataclasses import dataclass

from utils.util import Direction


@dataclass
class BracketSpec:
    """브래킷 프로토콜용 데이터클래스
    Attributes:
        bracket_type: # inner / outer
        install_type: # OpG / Tn
        gauge: 건식게이지
        direction: 방향
        name: 브래킷 풀네임
        index: 브래킷 인덱스
    """    # I / O
    bracket_type: str      # inner / outer
    install_type: str      # OpG / Tn
    gauge: float
    direction: Direction
    name: str
    index: int
