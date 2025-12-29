from core.BRACKET.bracket_specs import BracketSpec
from core.BRACKET.bracketdata import BracketElement
from core.FEEDER.feeder_spec import FeederSpec
from core.FEEDER.feederdata import FeederDATA
from core.MAST.mast_spec import MastSpec
from core.MAST.mastdata import MastDATA
from point3d import Point3d
from dataclasses import field
from utils.util import Direction
class PolePlaceDATA:
    """
        전주 설비 전체를 나타내는 개체 데이터 구조
        기둥, 브래킷, 금구류 포함 데이터
        Attributes:
            masts (MastDATA): 기둥 요소
            brackets (list[BracketElement]): 브래킷 목록
            feeders (FeederDATA): 급전선 설비들
            track_index: 선로번호
            pos (float): 전주 위치 (station)
            post_number (str): 전주 번호(0-1)
            gauge (float): 건식게이지(3.0,3.5,4.0,etc...)
            span: 경간
            ispreader: 평행틀(다중 브래킷 고정설비) 여부
            coord: 전주 좌표
            current_section: 현재 구간(개활지,에어섹션,에어조인트,정거장구간 등)
            direction: 설치방향
    """
    def __init__(self):
        self.masts: list[MastDATA] = []
        self.brackets: list[BracketElement] = []
        self.feeders: list[FeederDATA] =  []

        self.track_index: int = 0
        self.pos: float = 0.0
        self.post_number: str = ''
        self.gauge: float = 0.0
        self.span: int = 0
        self.ispreader: bool = False
        self.direction: Direction = Direction.LEFT

        self.coord: Point3d = Point3d(0, 0, 0)
        self.current_section = ''

    def apply_bracket(self, specs: list[BracketSpec]):
        self.brackets.clear()

        for spec in specs:
            bracket = BracketElement()
            bracket.element_type = spec.element_type
            bracket.name = spec.name
            bracket.index = spec.index
            bracket.direction = spec.direction
            self.brackets.append(bracket)

    def apply_feeder(self, specs: list[FeederSpec]):
        self.feeders.clear()
        for spec in specs:
            feeder = FeederDATA()
            feeder.index = spec.index
            feeder.name = spec.name
            feeder.direction = spec.direction
            feeder.positionx = spec.offset
            self.feeders.append(feeder)

    def apply_mast(self, specs: list[MastSpec]):
        self.masts.clear()
        for spec in specs:
            mast = MastDATA()
            mast.index = spec.index
            mast.direction = spec.direction
            self.masts.append(mast)


