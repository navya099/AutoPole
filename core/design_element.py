from dataclasses import dataclass

from utils.util import Direction

@dataclass
class DesignElement:
    """
    설계 단계에서 사용하는 논리적 요소
    Attributes:
        name: 요소 이름
        element_type: 요소 타입
        direction: 설치 방향
        code: 요소 코드
    """
    name: str = ''
    element_type: str = ''
    direction: Direction = Direction.LEFT
    code: int = 0