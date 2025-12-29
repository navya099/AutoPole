from core.BRACKET.bracket_specs import BracketSpec
from core.BRACKET.bracketdata import BracketElement
from core.FEEDER.feeder_spec import FeederSpec
from core.FEEDER.feederdata import FeederDATA
from core.MAST.mastdata import MastDATA
from utils.Vector3 import Vector3
from utils.util import Direction
class PoleDATA:
    """
        전주 설비 전체를 나타내는 데이터 구조
        기둥 브래킷 금구류 포함 데이터
        Attributes:
            mast (MastDATA): 기둥 요소
            brackets (list[BracketElement]): 브래킷 목록
            feeders (FeederDATA): 급전선 설비들

            track_index: 선로번호
            pos (float): 전주 위치 (station)
            post_number (str): 전주 번호
            current_curve (str): 현재 평면선형 직곡선상태(직선/곡선)
            radius (float): 곡선 반경
            cant (float): 캔트
            current_structure (str): 현재 구조물 상태 (토공/교량/터널)
            pitch (float): 구배
            current_airjoint (str): 에어조인트 구간(일반/에어조인트)
            gauge (float): 궤간
            span (int): 다음 전주 간 거리
            coord (Vector3): 전주의 3D 좌표
            ispreader (bool): 평행틀 유무
            direction (str): 전주 전역 방향 (R/L)
            vector (float): 벡터 각도 2D
    """
    def __init__(self):
        self.masts: list[MastDATA] = []
        self.brackets: list[BracketElement] = []
        self.feeders: list[FeederDATA] =  []

        self.track_index: int = 0
        self.pos: float = 0.0
        self.post_number: str = ''
        self.current_curve: str = ''
        self.radius: float = 0.0
        self.cant: float = 0.0
        self.current_structure: str = ''
        self.pitch: float = 0.0
        self.current_airjoint: str = ''
        self.gauge: float = 0.0
        self.span: int = 0


        self.coord: Vector3 = Vector3.Zero()
        self.ispreader: bool = False

        self.direction: Direction = Direction.LEFT
        self.vector: float = 0.0

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

