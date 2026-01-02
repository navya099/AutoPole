from config.catalog.bracket.bracket_catalog import BracketCatalog
from config.catalog.bracket.bracket_type_enum import BracketBaseType, BracketInstallType, BracketSpecialType, \
    BracketVariant
from core.BRACKET.bracket_specs import BracketSpec
from core.POLE.poledata import PolePlaceDATA

from utils.util import Direction

class BracketPolicy:
    def __init__(self):
        self.catalog = BracketCatalog()# 브래킷 데이터 클래스 가져오기

    def decide(self, index: int, pole, dataloader) -> list[BracketSpec]:
        """브래킷 정책 결정 메서드"""
        specs: list[BracketSpec] = []

        # 기본 브래킷
        base = self._decide_base(index, pole, dataloader)
        specs.append(base)

        return specs

    def _decide_base(self,index: int,pole: PolePlaceDATA, dataloader) -> BracketSpec:
        """단일 생성용 정책"""
        # i타입 bool판별
        is_i_type = self._is_i_type(index, pole)
        #현재 타입 판별
        current_type = self.get_current_type_and_bracket_type(is_i_type)
        # 설치 구분 판별
        install_type = self.get_installtype(pole.ref.structure_type)
        # 설치 방향
        direction = self.resolve_bracket_direction(pole.direction, install_type)
        # 구조물에 따라 스왑
        current_type = self.swap_type(direction, current_type, pole.ref.structure_type)
        #터널구간인경우
        specialtype = BracketSpecialType.TN if pole.ref.structure_type == '터널' else BracketSpecialType.NONE
        #코드 찾기
        mat = self.catalog.find_one(
            speed=dataloader.databudle.designspeed,
            base_type=current_type,
            special_type=specialtype,
            install_type=install_type,
            variant=BracketVariant.NONE,
            gauge=pole.gauge,
        )

        #결과 반환
        return BracketSpec(
            bracket_type=current_type,
            install_type=install_type,
            gauge=mat.gauge,
            direction=direction,
            name=mat.name,
            index=mat.code
        )

    @staticmethod
    def _is_i_type(index: int, pole: PolePlaceDATA) -> bool:
        """
        True  → I 타입
        False → O 타입
        """
        is_even = (index % 2 == 0)

        if pole.track_index == 0:  # 하선
            return not is_even  # 짝수=O, 홀수=I
        else:  # 상선
            return is_even  # 짝수=I, 홀수=O

    @staticmethod
    def get_installtype(current_structure: str) -> BracketInstallType:
        """설치 구분 및 게이지 판별 메서드
           반환 'OpG'
        Arguments:
            current_structure: 현재 구조물 정보
        Returns:
            BracketInstallType
            """
        if current_structure == '토공':
            install_type = BracketInstallType.OPG
        elif current_structure == '교량':
            install_type = BracketInstallType.OPG
        elif current_structure == '터널':
            install_type = BracketInstallType.TN
        else:
            install_type = BracketInstallType.NONE

        return install_type

    @staticmethod
    def get_current_type_and_bracket_type(is_i_type: bool) -> BracketBaseType:
        """i/o판별 메서드
            반환:  'I', 'inner'
        Arguments:
            is_i_type: i타입 여부
        Returns:
            tuple[str, str]
        """
        if is_i_type:
            current_type = BracketBaseType.I
        else:
            current_type = BracketBaseType.O

        return current_type

    @staticmethod
    def swap_type(poledirection, current_type: BracketBaseType, current_structure: str) -> BracketBaseType:
        """전주 방향(poledirection)이 반대일 경우와 터널일경우 브래킷 타입 전환"""
        if poledirection == 1 or current_structure == '터널':
            current_type = BracketBaseType.O if current_type == BracketBaseType.I else BracketBaseType.I
        return current_type

    @staticmethod
    def resolve_bracket_direction(direction, install_type):

        if direction == Direction.LEFT and install_type != BracketInstallType.TN:
            bracket_direction = Direction.LEFT
        else:
            bracket_direction = Direction.RIGHT

        return bracket_direction

    @staticmethod
    def get_sign(poledirection: int, bracket_type: str, current_structure: str) -> int:
        """현재 타입의 부호를 반환하는 메서드
            Parameters:
                poledirection (int): 전주방향(-1/1)
                bracket_type (str): 브래킷 타입 I,O
                current_structure (str): 현재 구조물
            Returns:
                int (-1 | 1)
        """
        is_tunnel = current_structure == '터널'

        if poledirection == -1:
            if bracket_type == BracketBaseType.I:
                return 1 if is_tunnel else -1
            elif bracket_type == BracketBaseType.O:
                return -1 if is_tunnel else 1
        elif poledirection == 1:
            if bracket_type == BracketBaseType.I:
                return 1
            elif bracket_type == BracketBaseType.O:
                return -1
        return 0