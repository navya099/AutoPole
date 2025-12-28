from core.element import Element


class MastDATA(Element):
    """
     전주 요소  Element상속
     Attributes:
         height(float):  전주높이(m)
         width(float): 전주폭(mm)
         fundermentalindex(int):  전주기초 오브젝트 인덱스
         fundermentaltype(str): 전주기초 타입
         fundermentaldimension(float): 전주기초치수
     """

    def __init__(self):
        super().__init__()
        self.height: float = 0.0
        self.width: float = 0.0
        self.fundermentalindex: int = 0
        self.fundermentaltype: str = ''
        self.fundermentaldimension: float = 0.0