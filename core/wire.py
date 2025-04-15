from .pole import BaseManager
from utils.util import *
import os
import sys
from fileio.jsonloader import ConfigManager
from types import MappingProxyType

# 현재 main.py 기준으로 상위 폴더에서 bveparser 경로 추가
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
bve_path = os.path.join(base_path, 'bveparser')

if bve_path not in sys.path:
    sys.path.insert(0, bve_path)
from OpenBveApi.Math.Vectors.Vector3 import Vector3

config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'span_data.json')


class WirePositionManager(BaseManager):
    def __init__(self, params, poledata):
        super().__init__(params, poledata)
        jsonmanager = ConfigManager(config_path)
        self.spandata = SpanDatabase(jsonmanager.get_config())
        self.wiredata = None

    def run(self):
        self.create_contact_wire()
        self.create_wire_common('af')
        self.create_wire_common('fpw')

    def create_contact_wire(self):
        data = self.poledata
        spandata = self.spandata
        wiredata = WireDataManager()  # 인스턴스 생성
        polyline_with_sta = [(i * 25, *values) for i, values in enumerate(self.coord_list)]
        for i in range(len(data.poles) - 1):
            pos = data.poles[i].pos
            next_pos = data.poles[i + 1].pos
            pos_coord, vector_pos = return_pos_coord(polyline_with_sta, pos)
            next_coord, next_vector = return_pos_coord(polyline_with_sta, next_pos)
            next_type = data.poles[i + 1].Brackets[0].type
            span = data.poles[i].span
            data.poles[i].coord = Vector3(*pos_coord)
            data.poles[i + 1].coord = Vector3(*next_coord)
            data.poles[i].vector = vector_pos
            current_structure = data.poles[i].current_structure
            contact_index = spandata.get_span_indices(self.designspeed, current_structure, 'contact', span)

            sign = self.get_sign(self.poledirection, data.poles[i].Brackets[0].type)
            next_sign = self.get_sign(self.poledirection, next_type)

            lateral_offset = sign * 0.2
            next_offset = next_sign * 0.2
            wiredata.wires[i].contactwire.stagger = lateral_offset

            planangle = calculate_curve_angle(polyline_with_sta, pos, next_pos, lateral_offset, next_offset)
            pitch_angle = change_permile_to_degree(data.poles[i].pitch)
            topdown_angle = calculate_slope(data.poles[i].coord.z, data.poles[i + 1].coord.z, span) - pitch_angle  # 전차
            wiredata.wires[i].contactwire.index = contact_index
            wiredata.wires[i].contactwire.xyangle = planangle
            wiredata.wires[i].contactwire.yzangle = topdown_angle
            block = WireDATA()
            wiredata.wires.append(block)
        self.wiredata = wiredata

    def create_wire_common(self, wire_type: str):
        data = self.poledata
        spandata = self.spandata
        wiredata = self.wiredata
        polyline_with_sta = [(i * 25, *values) for i, values in enumerate(self.coord_list)]

        for i in range(len(data.poles) - 1):
            pos = data.poles[i].pos
            next_pos = data.poles[i + 1].pos
            span = data.poles[i].span
            current_structure = data.poles[i].current_structure
            next_structure = data.poles[i + 1].current_structure
            gauge = data.poles[i].gauge
            index = spandata.get_span_indices(self.designspeed, current_structure, wire_type, span)
            offset = list(spandata.get_offset(self.designspeed, wire_type, current_structure))
            next_offset = list(spandata.get_offset(self.designspeed, wire_type, next_structure))

            # gauge에 따라 부호 적용
            if gauge < 0:
                offset[0] *= -1
                next_offset[0] *= -1
            # offset에 gauge를 더하여 보정. x만 y는 제외(offset은 토공을 기준으로 0)
            # offset 다시 tuple로 pack
            offset = (offset[0] + gauge, offset[1], 0)
            next_offset = (next_offset[0] + gauge, next_offset[1], 0)

            yaw, pitch, roll = self.calculate_wires_angle(
                polyline_with_sta, pos, next_pos, span, offset, next_offset
            )

            wire = getattr(wiredata.wires[i], f"{wire_type}wire")
            wire.name = wire_type
            wire.index = index
            wire.xoffset = offset[0]
            wire.yoffset = offset[1]
            wire.xyangle = yaw
            wire.yzangle = pitch

    @staticmethod
    def get_sign(poledirection, bracket_type):
        is_inner = bracket_type == 'I'
        return -1 if (poledirection == -1 and is_inner) or (poledirection != -1 and not is_inner) else 1

    @staticmethod
    def calculate_wires_angle(polyline_with_sta, pos, next_pos, length, start_offset, end_offset):
        """
        와이어 각도 계산 (Yaw, Pitch, Roll)
        :param end_offset:  끝점 오프셋 tuple or list (x,y,z)
        :param start_offset: 시작점 오프셋 tuple or list  (x,y,z)
        :param polyline_with_sta: 좌표선 정보 list
        :param pos: 시작 측점 int
        :param next_pos: 다음 측점 int
        :param length: 스팬 길이 int
        :return: yaw, pitch, roll (roll은 현재 None) float
        """
        if None not in (start_offset, end_offset):
            yaw = calculate_curve_angle(polyline_with_sta, pos, next_pos, start_offset[0], end_offset[0])
            pitch = math.degrees(math.atan((end_offset[1] - start_offset[1]) / length))
            roll = None  # 추후 횡단 경사 계산 등으로 구현 가능
            return yaw, pitch, roll
        return None, None, None


class WireDataManager:
    def __init__(self):
        self.wires = []
        wire = WireDATA()
        self.wires.append(wire)


class WireDATA:
    def __init__(self):
        self.contactwire = ContactWireElement()  # 전차선 요소
        self.afwire = FeederWireElement()  # 급전선요소
        self.fpwwire = AFwireElement()  # 보호선요소


class WireElement:
    def __init__(self):
        self.name = ''  # 이름
        self.height = 0.0  # 레일면에서의 높이
        self.length = 0  # 전선 길이
        self.xyangle = 0.0  # 전선의 평면각도
        self.index = 0  # 인덱스
        self.xoffset = 0.0  # x 오프셋
        self.yoffset = 0.0  # y 오프셋
        self.yzangle = 0.0  # 전선의 종단각도


class ContactWireElement(WireElement):
    def __init__(self):
        super().__init__()
        self.systemheihgt = 0.0  # 가고 :
        self.stagger = 0.0  # 편위


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
    def __init__(self, data: dict):
        self._data = MappingProxyType(data)

    def get_speed_codes(self):
        return list(self._data.keys())

    def get_wire_types(self, speed_code):
        return list(self._data[speed_code]["wires"].keys())

    def get_span_indices(self, speed_code, structure, wire_type, span_length):
        try:
            return self._data[str(speed_code)][structure][wire_type]["span_index"][str(span_length)]
        except KeyError:
            return ()

    def get_offset(self, speed_code, wire_type, structure_type):
        try:
            return tuple(self._data[str(speed_code)][structure_type][wire_type]["offset"])
        except KeyError:
            return 0, 0

    def get_prefix(self, speed_code):
        return self._data[speed_code].get("prefix", "")

    @staticmethod
    def get_span_description(span_length):
        span_map = {
            45: '경간 45m',
            50: '경간 50m',
            55: '경간 55m',
            60: '경간 60m'
        }
        return span_map.get(span_length, f"경간 {span_length}m")
