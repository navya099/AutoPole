class BVEFreeobj:
    """
    BVE 프리오브젝트 객체
    Attributes:
        name(str):  이름
        track_position: 블록 시작점
        rail_index: 레일인덱스
        object_index(int): 오브젝트 인덱스
        position_x(float): freeobj x offset
        position_y(float): freeobj y offset
        yaw(float): freeobj yaw
        pitch(float): freeobj pitch
        roll: freeobj roll
        """

    def __init__(self):
        self.name: str = ''
        self.track_position: float = 0.0
        self.object_index: int = 0
        self.rail_index: int = 0
        self.position_x: float = 0.0
        self.position_y: float = 0.0
        self.yaw: float = 0.0
        self.pitch: float = 0.0
        self.roll: float = 0.0