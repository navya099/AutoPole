from utils.util import Direction

class Element:
    """
    브래킷,전주 ,전선 요소 상위클래스
    Attributes:
        name(str):  이름
        index(int): 오브젝트 인덱스
        element_type(str) :  타입
        positionx(float): freeobj x offset
        positiony(float): freeobj y offset
        yaw(float): freeobj yaw
        pitch(float): freeobj pitch
        direction(Direction):  방향(Direction)
        """

    def __init__(self):
        self.name: str = ''
        self.index: int = 0
        self.element_type: str = ''
        self.positionx: float = 0.0
        self.positiony: float = 0.0
        self.yaw: float = 0.0  # 전선의 평면각도
        self.pitch: float = 0.0  # 전선의 종단각도
        self.roll: float = 0.0  # 전선의 roll각도

        self.direction: Direction = Direction.LEFT