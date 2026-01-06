from core.WIRE.wire_element import WireElement


class ContactWireElement(WireElement):
    """
        전차선 클래스 WireElement상속
        Attributes:
            systemheihgt (float): 가고
            stagger_start: 시점 전차선 편위
            stagger_end: 끝 전차선 편위
            height_start: 시작 전차선높이
            height_end: 끝 전차선높이
    """
    def __init__(self, start, end):
        super().__init__(start, end)
        self.systemheihgt: float = 0.0  # 가고 :
        self.stagger_start: float = 0.0
        self.stagger_end: float = 0.0
        self.height_start: float = 0.0
        self.height_end: float = 0.0
