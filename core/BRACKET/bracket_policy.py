from core.BRACKET.bracket_dictionary import Dictionaryofbracket
from core.BRACKET.bracket_specs import BracketSpec
from core.POLE.poledata import PoleDATA
from utils.util import Direction

class BracketPolicy:
    def __init__(self):
        self.dictionaryofbracket = Dictionaryofbracket()  # 브래킷 데이터 클래스 가져오기

    def decide(self, index: int, pole, dataloader) -> list[BracketSpec]:
        """브래킷 정책 결정 메서드"""
        specs: list[BracketSpec] = []

        # 기본 브래킷
        base = self._decide_base(index, pole, dataloader)
        specs.append(base)
        """
        징래 구현용 주석처리
        # 에어조인트 보강 브래킷
        if pole.current_airjoint == '에어조인트':
            aj = self._decide_airjoint(index, pole, dataloader)
            specs.append(aj)

        # 터널 보조 브래킷
        if pole.current_structure == '터널':
            tn = self._decide_tunnel(index, pole, dataloader)
            specs.append(tn)
        """
        return specs

    def _decide_base(self,index: int,pole: PoleDATA, dataloader) -> BracketSpec:
        """단일 생성용 정책"""
        #i타입 판별
        is_i_type = self._is_i_type(index, dataloader.databudle.mode)
        #현재 타입 판별 I ,INNER
        current_type, bracket_type = self.get_current_type_and_bracket_type(is_i_type)
        # 설치 구분 판별 OPG ,3.0
        install_type, gauge = self.get_installtype_and_gauge(pole.current_structure)
        # 설치 방향
        direction = self.resolve_bracket_direction(pole.direction, install_type)
        # 구조물에 따라 스왑
        current_type, bracket_type = self.swap_type(direction, current_type, bracket_type, pole.current_structure)

        #인덱스 얻기
        bracket_index = self.get_brackettype(
            speed=dataloader.databudle.designspeed,
            installtype=install_type,
            gauge= gauge,
            bracket_type= bracket_type)

        #이름 생성
        name = self._make_name(
            dataloader.databudle.designspeed,
            install_type,
            gauge,
            current_type
        )
        #결과 반환
        return BracketSpec(
            current_type, bracket_type,
            install_type, gauge,
            direction, name, bracket_index
        )

    def get_brackettype(self, speed: int, installtype: str, gauge: float, bracket_type: str) -> int:
        """브래킷 정보를 반환"""
        return self.dictionaryofbracket.get_bracket_number(speed, installtype, gauge, bracket_type)

    @staticmethod
    def _is_i_type(i, mode) -> bool:
        """
        모드에 따라 type여부 체크 메서드
        Returns:
             bool
        """
        if mode == 0:
            #  todo 아직 미완성
            raise NotImplementedError("mode=0 I/O 타입 판별 정책 미구현")
        else:
            is_i_type = (i % 2 == 1)
        return is_i_type

    @staticmethod
    def get_installtype_and_gauge(current_structure: str) -> tuple[str, float]:
        """설치 구분 및 게이지 판별 메서드
           반환 'OpG' , 3.0
        Arguments:
            current_structure: 현재 구조물 정보
        Returns:
            tuple[str, float]
            """
        if current_structure == '토공':
            install_type = 'OpG'
            gauge = 3.0
        elif current_structure == '교량':
            install_type = 'OpG'
            gauge = 3.5
        elif current_structure == '터널':
            install_type = 'Tn'
            gauge = 2.1
        else:
            install_type = ''
            gauge = 0.0

        return install_type, gauge

    @staticmethod
    def get_current_type_and_bracket_type(is_i_type: bool) -> tuple[str, str]:
        """i/o판별 메서드
            반환:  'I', 'inner'
        Arguments:
            is_i_type: i타입 여부
        Returns:
            tuple[str, str]
        """
        if is_i_type:
            current_type = 'I'
            bracket_type = 'inner'
        else:
            current_type = 'O'
            bracket_type = 'outer'

        return current_type, bracket_type

    @staticmethod
    def swap_type(poledirection, current_type: str, bracket_type: str, current_structure: str) -> tuple[str, str]:
        """전주 방향(poledirection)이 반대일 경우와 터널일경우 브래킷 타입 전환"""
        if poledirection == 1 or current_structure == '터널':
            current_type = 'O' if current_type == 'I' else 'I'
            bracket_type = 'outer' if bracket_type == 'inner' else 'inner'
        return current_type, bracket_type

    @staticmethod
    def _make_name(designspeed, install_type, gauge, current_type):
        """브래킷 풀네임 작성 메서드
            일반개소 = CaKo250-OpG3.0-I
            터널개소 = CaKo250-TN-I
        Arguments:
            designspeed: 설계속도
            install_type: 설치 위치 'OpG' ,'TN'
            gauge: 게이지
            current_type: 현재 타입 I . O
        Returns:
            str
        """
        if install_type == 'Tn':
            bracket_full_name = f'CaKo{designspeed}-{install_type}-{current_type}'
        else:
            bracket_full_name = f'CaKo{designspeed}-{install_type}{gauge}-{current_type}'
        return bracket_full_name

    @staticmethod
    def resolve_bracket_direction(direction, install_type):

        if direction == Direction.LEFT and install_type != 'Tn':
            bracket_direction = Direction.LEFT
        else:
            bracket_direction = Direction.RIGHT

        return bracket_direction