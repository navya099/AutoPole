from core.bve_element import Element
from core.design_element import DesignElement


class MastDesign(DesignElement):
    """전주 설계 정보
        Attributes:
            foundation_type: 기초 형식(사각기초,원형기초,특수기초)
            mast_role: 전주의 역할(단독주, 빔주, 인출주)

    """
    def __init__(self):
        super().__init__()
        self.foundation_type: str = ''
        self.mast_role: str = ''