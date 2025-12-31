from point3d import Point3d

class PoleRefData:
    """
    전주 '기준 위치' 데이터 (불변, 추상)
    Attributes:
        pos: 측점
        span: 다음 전주경간
        curve_type: 곡선
        radius: 곡선반경
        cant: 캔트
        pitch: 구배
        structure_type: 구조물
        center_coord: 선형 좌표 3d
        azimuth: 선형 진행 방위각
        section_info: 구간 정보
    """
    def __init__(self):
        self.pos: float = 0.0
        self.span: float = 0.0

        # 선형
        self.curve_type: str = ''
        self.radius: float = 0.0
        self.cant: float = 0.0
        self.pitch: float = 0.0

        # 구조물
        self.structure_type: str = ''

        # 공간 정보
        self.center_coord: Point3d = Point3d(0, 0, 0)
        self.azimuth: float = 0.0

        #구간 정보
        self.section_info: str = ''

    @property
    def is_last(self) -> bool:
        return self.span == 0

