from dataclasses import dataclass

from config.catalog.bracket.bracket_type_enum import BracketBaseType, BracketSpecialType, BracketVariant, \
    BracketInstallType


@dataclass(frozen=True)
class BracketMaterial:
    """기본 제품 카탈로그
    Attributes:
        code: 제품코드
        name: 제품명
        base_type: 기본 타입 (I, O, F)
        special_type: 특수 타입(AJ, AS, TN)
        install_type: 설치 구분(개활지, OPG 터널  tn)
        gauge: 건식게이지
    """
    code: int
    name: str
    base_type: BracketBaseType
    special_type: BracketSpecialType
    variant:BracketVariant
    install_type: BracketInstallType
    gauge: float
