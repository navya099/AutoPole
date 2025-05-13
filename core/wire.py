import traceback
from .pole import BaseManager, Element, PoleDATAManager
from utils.util import *
import os
from fileio.jsonloader import ConfigManager
from types import MappingProxyType
from utils.Vector3 import Vector3

config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'span_data.json')


class WirePositionManager(BaseManager):
    """전선 공통 기능을 관리하는 클래스 BaseManager상속

        Attributes:
            jsonmanager (ConfigManager): json 입출력을 위한 클래스
            spandata (SpanDatabase): (외부json spandata 저장하기 위한 클래스)
            wiredata (WireDataManager): WireData
            polyline_with_sta ( list[tuple[int, float, float, float]]): 측점 정보가 포함된 폴리선
            interpolatedata(CoordinateInterpolator): 폴리선에서 보간 좌표 계산을 위한 클래스
    """

    def __init__(self, params, poledata):
        super().__init__(params, poledata)
        self.jsonmanager = ConfigManager(config_path)
        self.spandata = SpanDatabase(self.jsonmanager.get_config())
        self.wiredata = None
        self.polyline_with_sta = [(i * 25, x, y, z) for i, (x, y, z) in enumerate(self.coord_list)]
        self.interpolatedata = CoordinateInterpolator(self.polyline_with_sta)

    def run(self):
        self.create_wires(['contact', 'af', 'fpw'])

    def create_wires(self, wire_types: list[str]):
        """전선데이터를 가공"""
        data: PoleDATAManager = self.poledata
        spandata = self.spandata
        wiredata = WireDataManager()  # 인스턴스 생성
        for i in range(len(data.poles) - 1):
            try:
                pos = data.poles[i].pos
                next_pos = data.poles[i + 1].pos

                self.interpolatedata.cal_interpolate(pos)
                pos_coord = self.interpolatedata.get_pos_coord()  # pos의 좌표
                vector_pos = self.interpolatedata.get_vector()  # pos의 각도

                self.interpolatedata.cal_interpolate(next_pos)
                next_pos_coord = self.interpolatedata.get_pos_coord()  # next_pos의 좌표

                span = data.poles[i].span  # 경간
                gauge = data.poles[i].gauge  # 건식게이지
                direction = data.poles[i].Brackets[0].direction  # 브래킷 방향
                current_structure = data.poles[i].current_structure  # 현재 구조물
                next_structure = data.poles[i + 1].current_structure  # 다음 구조물

                # 각 전선 종류별 처리
                for wire_type in wire_types:
                    if wire_type == 'contact':
                        self._set_contact_wire(
                            wiredata, i, data, spandata,
                            pos, next_pos, pos_coord, next_pos_coord,
                            vector_pos, span, current_structure
                        )
                    else:
                        self._set_common_wire(
                            wiredata, i, wire_type, spandata,
                            pos, next_pos, span,
                            current_structure, next_structure, direction
                        )

                # 좌표와 방향 저장
                data.poles[i].coord = Vector3(pos_coord.x, pos_coord.y, pos_coord.z)
                data.poles[i].vector = vector_pos

                block = WireDATA()
                wiredata.wires.append(block)

            except Exception as ex:
                error_message = (
                    f"예외 발생 in create_wire!\n"
                    f"인덱스: {i}\n"
                    f"위치: {pos}\n"
                    f"예외 종류: {type(ex).__name__}\n"
                    f"예외 메시지: {ex}\n"
                    f"전체 트레이스백:\n{traceback.format_exc()}"
                )
                logger.error(error_message)
                continue
        if len(wiredata.wires) > 0:
            # 속성에 추가
            self.wiredata = wiredata
            logger.debug(f"wiredata가 정상적으로 생성되었습니다. 전선 개수: {len(self.wiredata.wires)}")
        else:
            self.wiredata = None
            logger.error("wiredata가 None입니다! 데이터 생성에 실패했습니다.")

    def _set_contact_wire(self, wiredata, i, data, spandata,
                          pos, next_pos, pos_coord, next_pos_coord,
                          vector_pos, span, current_structure):
        current_bracket_type = data.poles[i].Brackets[0].element_type
        next_bracket_type = data.poles[i + 1].Brackets[0].element_type
        contact_index = spandata.get_span_indices(self.designspeed, current_structure, 'contact', span)
        sign = self.get_sign(self.poledirection, current_bracket_type)
        next_sign = self.get_sign(self.poledirection, next_bracket_type)
        lateral_offset = sign * 0.2
        next_offset = next_sign * 0.2
        planangle = self.interpolatedata.calculate_curve_angle(pos, next_pos, lateral_offset, next_offset)
        pitch_angle = change_permile_to_degree(data.poles[i].pitch)
        topdown_angle = calculate_slope(pos_coord.z, next_pos_coord.z, span) - pitch_angle

        wire = wiredata.wires[i].contactwire
        wire.stagger = lateral_offset
        wire.index = contact_index
        wire.yaw = planangle
        wire.pitch = topdown_angle
        wire.name = 'contact'

    def _set_common_wire(self, wiredata, i, wire_type, spandata,
                         pos, next_pos, span, current_structure, next_structure, direction: Direction):

        index = spandata.get_span_indices(self.designspeed, current_structure, wire_type, span)
        offset = list(spandata.get_offset(self.designspeed, wire_type, current_structure))
        next_offset = list(spandata.get_offset(self.designspeed, wire_type, next_structure))

        if direction == Direction.LEFT:
            offset[0] *= -1
            next_offset[0] *= -1

        offset = Vector3(offset[0], offset[1], 0)
        next_offset = Vector3(next_offset[0], next_offset[1], 0)
        wires_angle = self.calculate_wires_angle(pos, next_pos, span, offset, next_offset)

        wire = getattr(wiredata.wires[i], f"{wire_type}wire")
        wire.name = wire_type
        wire.index = index
        wire.positionx = offset.x
        wire.positiony = offset.y
        wire.yaw = wires_angle.x
        wire.pitch = wires_angle.y
        wire.roll = wires_angle.z
    @staticmethod
    def get_sign(poledirection: int, bracket_type: str):
        is_inner = bracket_type == 'I'
        return -1 if (poledirection == -1 and is_inner) or (poledirection != -1 and not is_inner) else 1

    def calculate_wires_angle(self, pos: int, next_pos: int, length: int, start_offset: Vector3,
                              end_offset: Vector3) -> Vector3:
        """
        와이어 각도 계산 (Yaw, Pitch, Roll)
        :param end_offset:  끝점 오프셋 Vector3
        :param start_offset: 시작점 오프셋 Vector3
        :param pos: 시작 측점 int
        :param next_pos: 다음 측점 int
        :param length: 스팬 길이 int
        :return: yaw, pitch, roll (Vector3)
        """
        wires_angle = Vector3.Zero()
        if None not in (start_offset, end_offset):
            yaw = self.interpolatedata.calculate_curve_angle(pos, next_pos, start_offset.x, end_offset.x)
            pitch = math.degrees(math.atan((end_offset.y - start_offset.y) / length))
            roll = 0.0  # 추후 횡단 경사 계산 등으로 구현 가능
            wires_angle = Vector3(yaw, pitch, roll)
        return wires_angle


class WireDataManager:
    """
    전선전체 총괄 클래스

    Attributes:
        wires (list): 개별 WireDATA 저장할 리스트
        """

    def __init__(self):
        self.wires = []
        wire = WireDATA()
        self.wires.append(wire)


class WireDATA:
    """
    전주 설비 전체를 나타내는 데이터 구조
    기둥 브래킷 금구류 포함 데이터
    Attributes:
        contactwire (ContactWireElement): 전차선 요소
        afwire (FeederWireElement): 급전선요소
        fpwwire (AFwireElement): 보호선요소
    """

    def __init__(self):
        self.contactwire = ContactWireElement()
        self.afwire = FeederWireElement()
        self.fpwwire = AFwireElement()


class WireElement(Element):
    def __init__(self):
        super().__init__()
        self.height: float = 0.0  # 레일면에서의 높이
        self.length: float = 0  # 전선 길이


class ContactWireElement(WireElement):
    def __init__(self):
        super().__init__()
        self.systemheihgt: float = 0.0  # 가고 :
        self.stagger: float = 0.0  # 편위


class FeederWireElement(WireElement):
    def __init__(self):
        super().__init__()


class AFwireElement(WireElement):
    def __init__(self):
        super().__init__()


def get_json_spandata():
    file = config_path  # 파이선 소스 폴더내의 config폴더에서 찾기
    configmanager = ConfigManager(file)
    spandata = configmanager.config
    return spandata


class SpanDatabase:
    """
    급전선 관련 데이터를 제공하는 클래스.
    주어진 데이터 딕셔너리를 읽기 전용으로 래핑하여 다양한 정보(설계 속도, 와이어 타입, 오프셋, 스팬 인덱스 등)를 반환한다.
    """

    def __init__(self, data: dict):
        """
        SpanDatabase 객체 초기화
        :param data: 설계 속도 및 구조에 따른 브래킷 데이터 딕셔너리
        """
        self._data = MappingProxyType(data)

    def get_speed_codes(self) -> list[str]:
        """
        사용 가능한 설계 속도 코드를 반환
        :return: 설계 속도 코드 목록
        """
        return list(self._data.keys())

    def get_wire_types(self, speed_code: int) -> list[str]:
        """
        주어진 설계 속도에 해당하는 와이어 타입 목록을 반환

        :param speed_code: 설계 속도 (예: 150, 250, 350)
        :return: 와이어 타입 리스트
        """
        return list(self._data[str(speed_code)]["wires"].keys())

    def get_span_indices(self, speed_code: int, structure: str, wire_type: str, span_length: int) -> tuple[int, ...]:
        """
        해당 조건에 맞는 스팬 인덱스를 반환

        :param speed_code: 설계 속도
        :param structure: 구조물 타입 (예: "토공", "교량", "터널")
        :param wire_type: 와이어 타입
        :param span_length: 경간 길이 (단위: m)
        :return: 스팬 인덱스 튜플, 존재하지 않으면 빈 튜플
        """
        try:
            return self._data[str(speed_code)][structure][wire_type]["span_index"][str(span_length)]
        except KeyError:
            return ()

    def get_offset(self, speed_code: int, wire_type: str, structure_type: str) -> tuple[float, float]:
        """
        해당 조건에 맞는 오프셋 좌표를 반환

        :param speed_code: 설계 속도
        :param wire_type: 와이어 타입
        :param structure_type: 구조물 타입
        :return: (좌측, 우측) 오프셋 튜플. 존재하지 않을 경우 (0, 0)
        """
        try:
            return tuple(self._data[str(speed_code)][structure_type][wire_type]["offset"])
        except KeyError:
            return 0, 0

    def get_prefix(self, speed_code: int) -> str:
        """
        해당 설계 속도에 대한 접두사(prefix)를 반환

        :param speed_code: 설계 속도 (문자열 또는 정수)
        :return: 접두사 문자열. 없을 경우 빈 문자열 반환
        """
        return self._data[str(speed_code)].get("prefix", "")

    @staticmethod
    def get_span_description(span_length: int) -> str:
        """
        경간 길이에 대한 설명 문자열 반환

        :param span_length: 경간 길이 (m)
        :return: '경간 50m' 등과 같은 설명 문자열
        """
        span_map = {
            45: '경간 45m',
            50: '경간 50m',
            55: '경간 55m',
            60: '경간 60m'
        }
        return span_map.get(span_length, f"경간 {span_length}m")
