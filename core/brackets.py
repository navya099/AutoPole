import traceback
from dataclasses import dataclass
from core.pole import BaseManager, PoleDATAManager, BracketElement
from utils.logger import logger
from utils.util import Direction


class BracketManager(BaseManager):
    """
     가동브래킷매니저 BaseManager상속
     Attributes:
         dictionaryofbracket(Dictionaryofbracket): 가동브래킷 데이터 딕셔너리

    """

    def __init__(self, dataloader, poledata):
        super().__init__(dataloader, poledata)
        self.dictionaryofbracket = Dictionaryofbracket()  # 브래킷 데이터 클래스 가져오기
        logger.debug(f'BracketManager 초기화 완료')

    def run(self):
        self.create_bracket()

    def get_brackettype(self, speed: int, installtype: str, gauge: float, bracket_type: str) -> int:
        """브래킷 정보를 반환"""
        return self.dictionaryofbracket.get_bracket_number(speed, installtype, gauge, bracket_type)

    def create_bracket(self):
        data:  PoleDATAManager = self.poledata

        for i in range(len(data.poles)):
            try:
                if self.loader.databudle.mode == 0:  # 기존 노선용
                    current_type, bracket_type, install_type, gauge = self.create_bracket_with_old_alignment(i, data)
                else:
                    count = self.loader.databudle.linecount
                    k = 0
                    for j in range(i , i + count):
                        current_type, bracket_type, install_type, gauge = self.create_bracket_with_new_alignment(j, data)

                        bracket_index = self.get_brackettype(
                            self.loader.databudle.designspeed, install_type, gauge, bracket_type
                        )
                        if install_type == 'Tn':
                            bracket_full_name = f'CaKo{self.loader.databudle.designspeed}-{install_type}-{current_type}'
                        else:
                            bracket_full_name = f'CaKo{self.loader.databudle.designspeed}-{install_type}{gauge}-{current_type}'

                        if data.poles[j].direction == Direction.LEFT and install_type != 'Tn':
                            bracket_direction = Direction.LEFT
                        else:
                            bracket_direction = Direction.RIGHT

                        #  속성지정
                        if not len(data.poles[i].Brackets) == count:
                            while len(data.poles[i].Brackets) < count:
                                data.poles[i].Brackets.append(BracketElement())

                        data.poles[i].Brackets[k].element_type = current_type
                        data.poles[i].Brackets[k].name = bracket_full_name
                        data.poles[i].Brackets[k].index = bracket_index

                        data.poles[i].gauge = gauge
                        data.poles[i].Brackets[k].direction = bracket_direction  # 개별 브래킷 방향
                        k += 1
            except Exception as ex:
                error_message = (
                    f"예외 발생 in create_bracket!\n"
                    f"인덱스: {i}\n"
                    f"예외 종류: {type(ex).__name__}\n"
                    f"예외 메시지: {ex}\n"
                    f"전체 트레이스백:\n{traceback.format_exc()}"
                )
                logger.error(error_message)
                continue
        logger.info(f'브래킷 생성이 완료됐습니다.')

    def check_poledirection(self):
        pass

    def create_bracket_with_new_alignment(self, i, data: PoleDATAManager) -> tuple[str, str, str, float]:
        """
        새 노선용 브래킷 생성 메서드

        Parameters:
            i (int): 반복문 인덱스
            data (PoleDATAManager): 전주 데이터 관리자 객체

        Returns:
            tuple[str, str, str, float]: (current_type, bracket_type, install_type, gauge)
        """
        is_i_type = self.check_current_is_i_type(i)
        current_type, bracket_type = self.get_current_type_and_bracket_type(is_i_type)
        current_structure = data.poles[i].current_structure
        # 전주 방향에 따라 타입 변경
        current_type, bracket_type = self.swap_type(current_type, bracket_type, current_structure)
        install_type, gauge = self.get_installtype_and_gauge(current_structure)
        return current_type, bracket_type, install_type, gauge

    def create_bracket_with_old_alignment(self, i, data: PoleDATAManager) -> tuple[str, str, str, float]:
        # todo 미완성 new_alignment복제
        raise NotImplementedError

    def check_current_is_i_type(self, i) -> bool:
        """
        모드에 따라 type여부 체크 메서드
        Returns:
             bool
        """
        if self.loader.databudle.mode == 0:
            #  todo 아직 미완성
            raise NotImplementedError
        else:
            is_i_type = (i % 2 == 1)
        return is_i_type

    @staticmethod
    def get_installtype_and_gauge(current_structure: str) -> tuple[str, float]:
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
        if is_i_type:
            current_type = 'I'
            bracket_type = 'inner'
        else:
            current_type = 'O'
            bracket_type = 'outer'

        return current_type, bracket_type

    def swap_type(self, current_type: str, bracket_type: str, current_structure: str) -> tuple[str, str]:
        """전주 방향(poledirection)이 반대일 경우와 터널일경우 브래킷 타입 전환"""
        if self.loader.databudle.poledirection == 1 or current_structure == '터널':
            current_type = 'O' if current_type == 'I' else 'I'
            bracket_type = 'outer' if bracket_type == 'inner' else 'inner'
        return current_type, bracket_type


@dataclass
class Bracket:
    inner: int  # I형
    outer: int  # O형
    flat_short: int  # F(S)
    flat_long: int  # F(L)
    airjoint_inner: int  # AJ-I
    airjoint_outer: int  # AJ-O


@dataclass
class GaugeBracketSet:
    gauge: float
    bracket: Bracket


@dataclass
class InstallTypeBracket:
    install_type: str  # 예: OpG, Tn
    gauge_brackets: dict[float, GaugeBracketSet]  # 게이지별 브래킷 정보


@dataclass
class PoleStructure:
    design_speed: int
    typename: str
    install_brackets: dict[str, InstallTypeBracket]  # OpG, Tn 등


# 사전 정의한 브래킷 정보 클래스(데이터클래스구조)
class Dictionaryofbracket:
    def __init__(self):
        self.brackettable = {
            150: PoleStructure(
                design_speed=150,
                typename="CaKo150",
                install_brackets={
                    "OpG": InstallTypeBracket(
                        install_type="OpG",
                        gauge_brackets={
                            3.0: GaugeBracketSet(
                                gauge=3.0,
                                bracket=Bracket(
                                    inner=1252,
                                    outer=1253,
                                    flat_short=1328,
                                    flat_long=1328,
                                    airjoint_inner=1252,
                                    airjoint_outer=1253
                                )
                            ),
                            3.5: GaugeBracketSet(
                                gauge=3.5,
                                bracket=Bracket(
                                    inner=1254,
                                    outer=1255,
                                    flat_short=1329,
                                    flat_long=1329,
                                    airjoint_inner=1254,
                                    airjoint_outer=1255
                                )
                            ),
                            2.1: GaugeBracketSet(
                                gauge=2.1,
                                bracket=Bracket(
                                    inner=1250,
                                    outer=1251,
                                    flat_short=1327,
                                    flat_long=1327,
                                    airjoint_inner=1250,
                                    airjoint_outer=1251
                                )
                            )
                        }
                    ),
                    "Tn": InstallTypeBracket(
                        install_type="Tn",
                        gauge_brackets={
                            2.1: GaugeBracketSet(  # 터널은 게이지 2.1만 존재
                                gauge=2.1,
                                bracket=Bracket(
                                    inner=941,
                                    outer=942,
                                    flat_short=1330,
                                    flat_long=1330,
                                    airjoint_inner=941,
                                    airjoint_outer=942
                                )
                            )
                        }
                    )
                }
            ),
            250: PoleStructure(
                design_speed=250,
                typename="CaKo250",
                install_brackets={
                    "OpG": InstallTypeBracket(
                        install_type="OpG",
                        gauge_brackets={
                            3.0: GaugeBracketSet(
                                gauge=3.0,
                                bracket=Bracket(
                                    inner=641,
                                    outer=642,
                                    flat_short=1284,
                                    flat_long=1285,
                                    airjoint_inner=1296,
                                    airjoint_outer=1297
                                )
                            ),
                            3.5: GaugeBracketSet(
                                gauge=3.5,
                                bracket=Bracket(
                                    inner=643,
                                    outer=644,
                                    flat_short=1286,
                                    flat_long=1287,
                                    airjoint_inner=1298,
                                    airjoint_outer=1299
                                )
                            ),
                            2.1: GaugeBracketSet(
                                gauge=2.1,
                                bracket=Bracket(
                                    inner=645,
                                    outer=646,
                                    flat_short=1288,
                                    flat_long=1289,
                                    airjoint_inner=1323,
                                    airjoint_outer=1324
                                )
                            )
                        }
                    ),
                    "Tn": InstallTypeBracket(
                        install_type="Tn",
                        gauge_brackets={
                            2.1: GaugeBracketSet(  # 터널은 게이지 2.1만 존재
                                gauge=2.1,
                                bracket=Bracket(
                                    inner=647,
                                    outer=648,
                                    flat_short=1290,
                                    flat_long=1291,
                                    airjoint_inner=1325,
                                    airjoint_outer=1326
                                )
                            )
                        }
                    )
                }
            ),
            350: PoleStructure(
                design_speed=350,
                typename="CaKo350",
                install_brackets={
                    "OpG": InstallTypeBracket(
                        install_type="OpG",
                        gauge_brackets={
                            3.0: GaugeBracketSet(
                                gauge=3.0,
                                bracket=Bracket(
                                    inner=570,
                                    outer=571,
                                    flat_short=578,
                                    flat_long=579,
                                    airjoint_inner=635,
                                    airjoint_outer=636
                                )
                            ),
                            3.5: GaugeBracketSet(
                                gauge=3.5,
                                bracket=Bracket(
                                    inner=572,
                                    outer=573,
                                    flat_short=580,
                                    flat_long=581,
                                    airjoint_inner=637,
                                    airjoint_outer=638
                                )
                            ),
                            2.1: GaugeBracketSet(
                                gauge=2.1,
                                bracket=Bracket(
                                    inner=1250,
                                    outer=1251,
                                    flat_short=1327,
                                    flat_long=1327,
                                    airjoint_inner=1250,
                                    airjoint_outer=1251
                                )
                            )
                        }
                    ),
                    "Tn": InstallTypeBracket(
                        install_type="Tn",
                        gauge_brackets={
                            2.1: GaugeBracketSet(  # 터널은 게이지 2.1만 존재
                                gauge=2.1,
                                bracket=Bracket(
                                    inner=574,
                                    outer=575,
                                    flat_short=582,
                                    flat_long=583,
                                    airjoint_inner=639,
                                    airjoint_outer=640
                                )
                            )
                        }
                    )
                }
            )
        }

    def get_structure(self, speed: int) -> PoleStructure:
        """
                설계 속도에 해당하는 구조를 반환합니다.

                Args:
                    speed (int): 설계 속도 (km/h)

                Returns:
                    PoleStructure: 해당 속도에 맞는 구조 정보
                """
        return self.brackettable.get(speed)

    def get_install_type(self, speed: int, install_type: str) -> InstallTypeBracket:
        """
                설계 속도와 설치 타입에 해당하는 설치 타입 정보를 반환합니다.

                Args:
                    speed (int): 설계 속도 (km/h)
                    install_type (str): 설치 타입 (예: "OpG", "Tn")

                Returns:
                    InstallTypeBracket: 해당 설치 타입에 맞는 정보
                """

        structure = self.get_structure(speed)
        if structure:
            return structure.install_brackets.get(install_type)

    def get_gauge_set(self, speed: int, install_type: str, gauge: float) -> GaugeBracketSet:
        """
                설계 속도, 설치 타입 및 게이지에 맞는 게이지 세트를 반환합니다.

                Args:
                    speed (int): 설계 속도 (km/h)
                    install_type (str): 설치 타입 (예: "OpG", "Tn")
                    gauge (float): 게이지 (m)

                Returns:
                    GaugeBracketSet: 해당 조건에 맞는 게이지 브래킷 세트
                """

        install = self.get_install_type(speed, install_type)
        if install:
            return install.gauge_brackets.get(gauge)

    def get_bracket_number(self, speed: int, install_type: str, gauge: float, bracket_type: str) -> int:
        """
                브래킷 인덱스를 반환합니다.

                Args:
                    speed (int): 설계 속도 (km/h)
                    install_type (str): 설치 타입 (예: "OpG", "Tn")
                    gauge (float): 게이지 (m)
                    bracket_type (str): 반환하려는 브래킷의 종류 (예: "inner", "outer")

                Returns:
                    int: 해당 브래킷 번호
                """
        gauge_set = self.get_gauge_set(speed, install_type, gauge)
        if gauge_set:
            return getattr(gauge_set.bracket, bracket_type, None)
