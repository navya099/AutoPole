import random
import traceback

import pandas as pd

from fileio.dataloader import DataLoader
from fileio.fileloader import TxTFileHandler
from utils.util import *
from utils.Vector3 import Vector3
from typing import Optional


class AirJoint(Enum):
    START = "에어조인트 시작점 (1호주)"
    POINT_2 = "에어조인트 (2호주)"
    MIDDLE = "에어조인트 중간주 (3호주)"
    POINT_4 = "에어조인트 (4호주)"
    END = "에어조인트 끝점 (5호주)"


class BaseManager:
    """MastManager와 BracketManager의 공통 기능을 관리하는 부모 클래스

    Attributes:
        poledata (Optional[PoleDATAManager]): 전주 데이터
        loader (DataLoader): 데이터로더 객체
    """

    def __init__(self, dataloader: DataLoader, poledata: Optional['PoleDATAManager'] = None):
        self.poledata: Optional[PoleDATAManager] = poledata  # ✅ PoleDATAManager.poledata 인스턴스를 가져옴
        self.loader = dataloader  # ✅ DataLoader 인스턴스를 가져옴


class PolePositionManager(BaseManager):
    """전주 생성기능을 관리하는 클래스

    Attributes:
        pole_positions (list): 전주 위치 데이터
        airjoint_list (list): 에어조인트 위치 데이터
        post_number_lst (list): 전주번호 데이터
        posttype_list (list): 전주타입 리스트
    """

    def __init__(self, dataloader):
        super().__init__(dataloader)
        self.pole_positions: list[int] = []
        self.airjoint_list: list[tuple[int, str]] = []
        self.post_number_lst: list[str] = []
        self.posttype_list: list[tuple[int, str]] = []
        logger.debug(f'PolePositionManager 초기화 완료')

    def run(self):
        self.generate_positions()
        self.create_pole()

    def generate_positions(self):
        """
        모드에 따라 pole_positions을 생성하는 메소드
        """
        if self.loader.databudle.mode == 1:  # 새 노선용
            self.pole_positions = self.distribute_pole_spacing_flexible(
                self.loader.bvealignment.startkm, self.loader.bvealignment.endkm, spans=(45, 50, 55, 60)
            )
            self.airjoint_list = self.define_airjoint_section(self.pole_positions)
            self.post_number_lst = self.generate_postnumbers(self.pole_positions)
            logger.info(f'전주 포지션 생성 완료\n pole_positions 갯수:{len(self.pole_positions)}\n,'
                        f'airjoint_list 갯수:{len(self.airjoint_list)}\n,'
                        f'post_number_lst 갯수:{len(self.post_number_lst)}')
        else:  # mode 0  기존 노선용
            # Load from file
            raise NotImplementedError

    def get_pole_data(self):
        return self.poledata

    def create_pole(self):
        """전주 위치 데이터를 가공"""

        data = PoleDATAManager()  # 인스턴스 생성
        for i in range(len(self.pole_positions)):
            try:
                pos = self.pole_positions[i]  # 전주 위치 station
                if i < len(self.pole_positions) - 1:
                    next_pos = self.pole_positions[i + 1]  # 다음 전주 위치 station
                    current_span = next_pos - pos  # 현재 전주 span
                else:
                    next_pos = 0
                    current_span = 0  # 현재 전주 span

                # 현재 위치의 구조물 및 곡선 정보 가져오기
                current_structure = self.loader.structures.get_structure_type_at(pos)  # 현재 위치의 구조물
                current_curve = self.loader.bvealignment.get_current_curve_string(pos)  # 현재 전주 위치의 곡선유뮤
                current_radius = self.loader.bvealignment.get_curve_radius(pos)  # 현재 전주 위치의 곡선반경
                current_cant = self.loader.bvealignment.get_curve_cant(pos)  # 현재 전주 위치의 캔트
                current_slope = self.loader.bvealignment.get_current_pitch_string(pos)  # 현재 전주 위치의 구배유뮤
                current_pitch = self.loader.bvealignment.get_pitch_permille(pos)  # 현재 전주 위치의 구배

                current_airjoint = check_isairjoint(pos, self.airjoint_list)  # 현재 전주 위치의 AJ
                post_number = find_post_number(self.post_number_lst, pos)  # 현재 전주넘버

                # final
                data.poles[i].pos = pos
                data.poles[i].span = current_span
                data.poles[i].current_structure = current_structure  # 현재 전주 위치의 구조물
                data.poles[i].current_curve = current_curve
                data.poles[i].radius = current_radius
                data.poles[i].cant = current_cant
                data.poles[i].pitch = float(current_pitch)
                data.poles[i].current_airjoint = current_airjoint
                data.poles[i].post_number = post_number
                if self.loader.databudle.poledirection == -1:
                    data.poles[i].direction = Direction.LEFT
                else:
                    data.poles[i].direction = Direction.RIGHT  # 전체 방향

                block = PoleDATA()  # 폴 블록 생성
                data.poles.append(block)
            except Exception as ex:
                error_message = (
                    f"예외 발생 in create_pole!\n"
                    f"인덱스: {i}\n"
                    f"위치: {pos}\n"
                    f"예외 종류: {type(ex).__name__}\n"
                    f"예외 메시지: {ex}\n"
                    f"전체 트레이스백:\n{traceback.format_exc()}"
                )
                logger.error(error_message)
                continue
        # 마지막 블록 제거
        data.poles.pop()
        if len(data.poles) > 0:
            # 속성에 추가
            self.poledata = data
            logger.debug(f"poledata가 정상적으로 생성되었습니다. 전주 개수: {len(self.poledata.poles)}")
        else:
            self.poledata = None
            logger.error("poledata가 None입니다! 데이터 생성에 실패했습니다.")

    @staticmethod
    def generate_postnumbers(lst: list[int]) -> list[tuple[int, str]]:
        postnumbers = []
        prev_km = -1
        count = 0

        for number in lst:
            km = number // 1000  # 1000으로 나눈 몫이 같은 구간
            if km == prev_km:
                count += 1  # 같은 구간에서 숫자 증가
            else:
                prev_km = km
                count = 1  # 새로운 구간이므로 count를 0으로 초기화

            postnumbers.append((number, f'{km}-{count}'))

        return postnumbers

    def load_pole_positions_from_file(self) -> None:
        """txt 파일을 읽고 곧바로 '측점', '전주번호', '타입', '에어조인트' 정보를 반환하는 함수"""

        # 텍스트 파일(.txt) 읽기
        txtfile_handler = TxTFileHandler()
        txtfile_handler.select_file("미리 정의된 전주 파일 선택", [("txt files", "*.txt"), ("All files", "*.*")])
        txt_filepath = txtfile_handler.get_filepath()

        df_curve = pd.read_csv(txt_filepath, sep=",", header=0, names=['측점', '전주번호', '타입', '에어조인트'])

        # 곡선 구간 정보 저장
        self.pole_positions = df_curve['측점'].tolist()
        self.post_number_lst = list(zip(df_curve['측점'], df_curve['전주번호']))
        self.posttype_list = list(zip(df_curve['측점'], df_curve['타입']))
        self.airjoint_list = [(row['측점'], row['에어조인트']) for _, row in df_curve.iterrows() if row['에어조인트'] != '일반개소']

    # GET 메소드 추가
    def get_all_pole_data(self) -> dict[str, list]:
        """전주 관련 모든 데이터를 반환"""
        return {
            "pole_positions": self.pole_positions,
            "airjoint_list": self.airjoint_list,
            "post_number_lst": self.post_number_lst,
            "posttype_list": self.posttype_list,
        }

    @staticmethod
    def distribute_pole_spacing_flexible(
            start_km: float, end_km: float, spans: tuple[int, ...] = (45, 50, 55, 60)
    ) -> list[int]:
        """
        45, 50, 55, 60m 범위에서 전주 간격을 균형 있게 배분하여 전체 구간을 채우는 함수
        마지막 전주는 종점보다 약간 앞에 위치할 수도 있음.

        :param start_km: 시작점 (km 단위)
        :param end_km: 끝점 (km 단위)
        :param spans: 사용 가능한 전주 간격 튜플 (기본값: 45, 50, 55, 60)
        :return: 전주 간격 리스트, 전주 위치 리스트
        """
        if spans is None:
            spans = (45, 50, 55, 60)

        start_m = int(start_km)  # km → m 변환
        end_m = int(end_km)

        positions = [start_m]
        selected_spans = []
        current_pos = start_m

        while current_pos < end_m:
            possible_spans = list(spans)  # 사용 가능한 간격 리스트 (45, 50, 55, 60)
            random.shuffle(possible_spans)  # 랜덤 배치

            for span in possible_spans:
                if current_pos + span > end_m:
                    continue  # 종점을 넘어서면 다른 간격을 선택

                positions.append(current_pos + span)
                selected_spans.append(span)
                current_pos += span
                break  # 하나 선택하면 다음으로 이동

            # 더 이상 배치할 간격이 없으면 종료
            if current_pos + min(spans) > end_m:
                break

        return positions

    @staticmethod
    def define_airjoint_section(positions: list[int]) -> list[tuple[int, str]]:
        """
        에어조인트(AirJoint) 위치를 정의하는 정적 메서드.

        주어진 전주 위치 목록(positions) 중에서 특정 간격(airjoint_span = 1600m)을 기준으로,
        조건을 만족하는 지점부터 최대 5개의 전주 위치에 에어조인트 태그를 할당하여 리스트로 반환한다.

        조건:
            - 현재 위치가 airjoint_span의 배수(±100m 허용 오차)와 가까운 경우에만 에어조인트 설정.

        에어조인트 태그 순서:
            - START, POINT_2, MIDDLE, POINT_4, END

        Args:
            positions (list[int]): 전주 위치(정수값, m단위) 리스트

        Returns:
            list[tuple[int, str]]: (위치, 에어조인트 태그) 쌍의 리스트
        """
        airjoint_list: list[tuple[int, str]] = []
        airjoint_span: int = 1600  # 에어조인트 설치 간격(m)

        def is_near_multiple_of_number(number: int, tolerance: int = 100) -> bool:
            """
            숫자가 주어진 간격(airjoint_span)의 배수에 근접한지 판단하는 내부 함수.

            Args:
                number (int): 판별할 숫자
                tolerance (int, optional): 허용 오차. 기본값은 100.

            Returns:
                bool: 배수에 근접하면 True, 아니면 False
            """
            remainder = number % airjoint_span
            return number > airjoint_span and (remainder <= tolerance or remainder >= (airjoint_span - tolerance))

        i = 0
        while i < len(positions) - 1:
            pos = positions[i]
            if is_near_multiple_of_number(pos):
                next_values = positions[i + 1:min(i + 6, len(positions))]
                tags = [
                    AirJoint.START.value,
                    AirJoint.POINT_2.value,
                    AirJoint.MIDDLE.value,
                    AirJoint.POINT_4.value,
                    AirJoint.END.value
                ]
                airjoint_list.extend(list(zip(next_values, tags[:len(next_values)])))
                i += 5  # 다음 다섯 개를 건너뜀
            else:
                i += 1

        return airjoint_list


class PoleDATAManager:  # 전체 총괄
    """
    전주전체 총괄 클래스

    Attributes:
        poles (list): 개별 PoleDATA 저장할 리스트
    """

    def __init__(self):
        self.poles = []
        pole = PoleDATA()
        self.poles.append(pole)


class PoleDATA:
    """
        전주 설비 전체를 나타내는 데이터 구조
        기둥 브래킷 금구류 포함 데이터
        Attributes:
            mast (MastDATA): 기둥 요소
            Brackets (list[BracketElement]): 브래킷 목록
            feeder (FeederDATA): 급전선 설비
            pos (float): 전주 위치 (station)
            post_number (str): 전주 번호
            current_curve (str): 곡선 구간 여부(직선/곡선)
            radius (float): 곡선 반경
            cant (float): 캔트
            current_structure (str): 구조물 상태 (토공/교량/터널)
            pitch (float): 구배
            current_airjoint (str): 에어조인트 여부(일반/에어조인트)
            gauge (float): 궤간
            span (int): 전주 간 거리
            coord (Vector3): 전주의 3D 좌표
            ispreader (bool): 평행틀 유무
            direction (str): 방향 (R/L)
            vector (float): 벡터 각도 2D
    """

    def __init__(self):
        self.mast: MastDATA = MastDATA()  # 기둥 요소
        self.Brackets: list[BracketElement] = []  # 브래킷 리스트
        bracketdata = BracketElement()  # 브래킷 인스턴스 생성
        self.Brackets.append(bracketdata)

        self.feeder: FeederDATA = FeederDATA()  # 급전선 설비
        self.pos: float = 0.0  # 전주 위치 (station)
        self.post_number: str = ''  # 전주 번호
        self.current_curve: str = ''  # 곡선 여부
        self.radius: float = 0.0  # 곡선 반경
        self.cant: float = 0.0  # 캔트
        self.current_structure: str = ''  # 구조물 (교량, 터널 등)
        self.pitch: float = 0.0  # 구배
        self.current_airjoint: str = ''  # 에어조인트 위치
        self.gauge: float = 0.0  # 궤간
        self.span: int = 0  # 전주 간 거리

        self.coord: Vector3 = Vector3.Zero()  # 3D 좌표
        self.ispreader: bool = False  # 스프레더 여부
        self.direction: Direction = Direction.LEFT  # 방향 (R, L)
        self.vector: float = 0.0  # 벡터 각도


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


class BracketElement(Element):
    """
    브래킷 요소 Element상속
    """

    def __init__(self):
        super().__init__()


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


class FeederDATA(Element):
    """급전선 설비 데이터를 설정하는 클래스 Element 상속"""

    def __init__(self):
        super().__init__()


class MastManager(BaseManager):
    """전주(Mast) 데이터를 설정하는 클래스"""

    def __init__(self, dataloader, poledata):
        super().__init__(dataloader, poledata)

    def run(self):
        self.create_mast()

    def create_mast(self):
        data = self.poledata
        for i in range(len(data.poles)):
            try:
                current_structure = data.poles[i].current_structure
                mast_index, mast_name = get_mast_type(self.loader.databudle.designspeed, current_structure)
                data.poles[i].mast.name = mast_name
                data.poles[i].mast.index = mast_index
                data.poles[i].mast.direction = data.poles[i].Brackets[0].direction

            except Exception as ex:
                error_message = (
                    f"예외 발생 in create_mast!\n"
                    f"인덱스: {i}\n"
                    f"예외 종류: {type(ex).__name__}\n"
                    f"예외 메시지: {ex}\n"
                    f"전체 트레이스백:\n{traceback.format_exc()}"
                )
                logger.error(error_message)
                continue


class FeederManager(BaseManager):
    """급전선 설비(전선x) 데이터를 설정하는 클래스"""

    def __init__(self, dataloader, poledata):
        super().__init__(dataloader, poledata)

    def run(self):
        self.create_feeder()

    def create_feeder(self):
        data = self.poledata
        speed = self.loader.databudle.designspeed
        # 구조별 설계속도에 따른 피더 인덱스 맵
        feeder_map = {
            ('토공', 150): 1234,
            ('토공', 250): 1234,
            ('토공', 350): 597,
            ('교량', 150): 1234,
            ('교량', 250): 1234,
            ('교량', 350): 597,
            ('터널', 150): 1249,
            ('터널', 250): 1249,
            ('터널', 350): 598,
        }

        for i in range(len(data.poles)):
            current_structure = data.poles[i].current_structure

            feederindex = feeder_map.get((current_structure, speed), 1234)
            data.poles[i].feeder.index = feederindex
            data.poles[i].feeder.name = '급전선 지지물'
            data.poles[i].feeder.direction = data.poles[i].direction
            data.poles[i].feeder.positionx = data.poles[i].gauge * data.poles[i].feeder.direction.value
