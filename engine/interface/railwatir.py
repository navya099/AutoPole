from dataclasses import dataclass
from typing import Optional, Any

from point3d import Point3d
from utils.util import Direction

@dataclass
class RailwayIR:
    """추상 설계 렌더 인터페이스
    Attributes:
        category: 카테고리 # mast / bracket / feeder / fitting
        code: 제품 코드
        track: 선로번호
        position: 원점 좌표
        direction: 설치방향
        name: 이름
        meta: 메타정보
        geometry: 지오메트리 정보
    """
    category: str
    code: int
    track: int
    position: Point3d | None = None
    direction: Direction | None = None
    name: str | None = None
    meta: dict | None = None
    geometry: Any | None = None
