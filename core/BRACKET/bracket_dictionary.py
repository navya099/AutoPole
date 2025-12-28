# 사전 정의한 브래킷 정보 클래스(데이터클래스구조)
from core.BRACKET.brackets import PoleStructure, InstallTypeBracket, GaugeBracketSet, Bracket


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