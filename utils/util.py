import math
from enum import Enum

from utils.logger import logger
from typing import Literal, List, Tuple
from utils.Vector3 import Vector3


def check_isairjoint(input_sta, airjoint_list):
    for data in airjoint_list:
        sta, tag = data
        if input_sta == sta:
            return tag
    return '일반개소'


def get_block_index(current_track_position, block_interval=25):
    """현재 트랙 위치를 블록 인덱스로 변환"""
    return math.floor(current_track_position / block_interval + 0.001) * block_interval


def find_last_block(data: str) -> int:
    """
    주어진 문자열 리스트의 마지막 요소에서 블록 값을 추출하여 반환합니다.

    :param data: 예: ['25.0,0.0,0.0', '30.0,1.0,2.0']
    :return: 마지막 블록의 float 값 (예: 30.0)
    """
    if not data:
        raise ValueError("입력 데이터가 비어 있습니다.")

    try:
        last_line = data[-1]
        block_value = float(last_line.split(',')[0])
        return int(block_value)
    except (IndexError, ValueError) as e:
        raise ValueError(f"마지막 블록 값을 파싱하는 중 오류 발생: {e}")


def find_post_number(lst, pos):
    for arg in lst:
        if arg[0] == pos:
            return arg[1]


def buffered_write(filename, lines):
    """파일 쓰기 버퍼 함수"""
    filename = "C:/TEMP/" + filename
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)


def get_mast_type(speed: int, current_structure: str) -> tuple[int, str]:
    # 전주 인덱스 딕셔너리(idx,comment)
    mast_dic = {
        150: {
            'prefix': 'Cako150',
            '토공': (1370, 'P-10"x7t-9m'),
            '교량': (1376, 'P-12"x7t-8.5m'),
            '터널': (1400, '터널하수강'),
        },
        250: {
            'prefix': 'Cako250',
            '토공': (1370, 'P-10"x7t-9m'),
            '교량': (1376, 'P-12"x7t-8.5m'),
            '터널': (1400, '터널하수강'),
        },
        350: {
            'prefix': 'Cako350',  # 350
            '토공': (619, 'H형주-208X202'),
            '교량': (620, 'H형주-250X255'),
            '터널': (621, '터널하수강'),
        }
    }
    mast_data = mast_dic.get(speed, mast_dic[250])
    mast_index, mast_name = mast_data.get(current_structure, ("", "알 수 없는 구조"))

    return mast_index, mast_name


class CoordinateInterpolator:
    """폴리선 보간 기능을 수행하는 유틸클래스
        Attributes:
            bvealignment (BVEAlignment): bve선형객체
            interpolate_coord (Vector3): 보간된 점의 좌표 Vector3
            origin_coord (Vector3): 보간된 점의 시작점 좌표 Vector3
            vector (float): 시작점의 방향벡터(각도)
    """
    from geometry.alignment import BVEAlignment

    def __init__(self, bvealignment: BVEAlignment):
        self.bvealignment = bvealignment
        self.interpolate_coord: Vector3 = Vector3.Zero()
        self.origin_coord: Vector3 = Vector3.Zero()
        self.vector: float = 0.0
        self.interval = 25.0

    def cal_interpolate(self, target_sta: int):
        """
        BVEAlignment 내의 좌표리스트를 기반으로, 주어진 거리에서 보간 위치를 계산합니다.
        self.interpolate_coord, self.origin_coord, self.vector를 설정합니다.
        """
        current_index = self.bvealignment.get_index(target_sta)
        next_index = current_index + 1
        current_pos = self.bvealignment.get_coord_at_index(current_index)
        next_pos = self.bvealignment.get_coord_at_index(next_index)

        if current_pos is None or next_pos is None:
            logger.error(f"STA {target_sta} is out of polyline range.")
            raise ValueError(f"STA {target_sta} is out of polyline range.")

        current_sta = self.bvealignment.get_station_at_index(current_index)
        next_sta = current_sta + 25
        t = target_sta - current_sta
        self.vector = calculate_bearing(current_pos.x, current_pos.y, next_pos.x, next_pos.y)
        x, y = calculate_destination_coordinates(current_pos.x, current_pos.y, self.vector, t)
        z = self.cal_interpolate_height(current_pos.z, next_pos.z, next_sta - current_sta, t)
        self.interpolate_coord = Vector3(x, y, z)
        self.origin_coord = current_pos

    def get_elevation_pos(self) -> float:
        """
        보간된 높이(float)를 반환합니다.
        """
        return self.interpolate_coord.z

    def get_origin_coord(self) -> Vector3:
        """
        보간점 사이의 시작 좌표(Vector3)를 반환합니다.
        """
        return self.origin_coord

    @staticmethod
    def cal_interpolate_height(start_z: float, end_z: float, total_length: float, distance: float) -> float:
        """
        두 점 사이의 높이를 선형 보간하여, 지정된 거리 지점의 높이를 반환합니다.
        """
        return start_z + ((end_z - start_z) / total_length) * distance

    def get_pos_coord(self) -> Vector3:
        """
        보간점의 좌표(Vector3)를 반환합니다.
        """
        return self.interpolate_coord

    def get_vector(self) -> float:
        """
        보간점 사이의 시작점 각도를 반환합니다.
        """
        return self.vector

    def calculate_curve_angle(self, pos: int, next_pos: int, stagger1: float, stagger2: float) -> float:
        """
        전차선의 좌우 offset을 고려한 yaw 각도 계산 함수
        :param pos: 시작 측점
        :param next_pos: 끝 측점
        :param stagger1: 시작점 좌우 offset
        :param stagger2: 끝점 좌우 offset
        :return: yaw angle (degrees)
        """
        final_anlge = 0.0  # 변수초기화

        # 시작pos와 끝 pos의 좌표와 폴리선 벡터 반환
        self.cal_interpolate(pos)
        point_a = self.get_pos_coord()
        vector_a = self.get_vector()

        self.cal_interpolate(next_pos)
        point_b = self.get_pos_coord()
        vector_b = self.get_vector()

        if point_a and point_b:
            # offset 점 계산
            offset_point_a = calculate_offset_point(vector_a, point_a, stagger1)
            offset_point_b = calculate_offset_point(vector_b, point_b, stagger2)

            # offset점끼리의 각도
            a_b_angle = calculate_bearing(offset_point_a.x, offset_point_a.y, offset_point_b.x, offset_point_b.y)

            # 최종 각도
            final_anlge = vector_a - a_b_angle
        return final_anlge


def calculate_bearing(x1: float, y1: float, x2: float, y2: float) -> float:
    # Calculate the bearing (direction) between two points in Cartesian coordinates
    dx = x2 - x1
    dy = y2 - y1
    bearing = math.degrees(math.atan2(dy, dx))
    return bearing


def calculate_destination_coordinates(x1: float, y1: float, bearing: float, distance: float) -> tuple[float, float]:
    # Calculate the destination coordinates given a starting point, bearing, and distance in Cartesian coordinates
    angle = math.radians(bearing)
    x2 = x1 + distance * math.cos(angle)
    y2 = y1 + distance * math.sin(angle)
    return x2, y2


def get_wire_span_data(designspeed, currentspan, current_structure):
    """ 경간에 따른 wire 데이터 반환 """
    # SPEED STRUCTURE span 45, 50, 55, 60
    span_data = {
        150: {
            'prefix': 'Cako150',
            '토공': (592, 593, 594, 595),  # 가고 960
            '교량': (592, 593, 594, 595),  # 가고 960
            '터널': (614, 615, 616, 617)  # 가고 710
        },
        250: {
            'prefix': 'Cako250',
            '토공': (484, 478, 485, 479),  # 가고 1200
            '교량': (484, 478, 485, 479),  # 가고 1200
            '터널': (494, 495, 496, 497)  # 가고 850
        },
        350: {
            'prefix': 'Cako350',
            '토공': (488, 489, 490, 491),  # 가고 1400
            '교량': (488, 489, 490, 491),  # 가고 1400
            '터널': (488, 489, 490, 491)  # 가고 1400
        }
    }

    # DESIGNSPEED에 맞는 구조 선택 (기본값 250 사용)
    span_values = span_data.get(designspeed, span_data[250])

    # current_structure에 맞는 값 추출
    current_structure_list = span_values[current_structure]

    # currentspan 값을 통해 급전선 fpw 인덱스를 추출
    span_index_mapping = {
        45: (0, '경간 45m', 1236, 1241),
        50: (1, '경간 50m', 1237, 1242),
        55: (2, '경간 55m', 1238, 1243),
        60: (3, '경간 60m', 1239, 1244)
    }

    # currentspan이 유효한 값인지 확인
    if currentspan not in span_index_mapping:
        raise ValueError(f"Invalid span value '{currentspan}'. Valid values are 45, 50, 55, 60.")

    # currentspan에 해당하는 인덱스 및 주석 추출
    idx, comment, feeder_idx, fpw_idx = span_index_mapping[currentspan]
    # idx 값을 current_structure_list에서 가져오기
    idx_value = current_structure_list[idx]

    return idx_value, comment, feeder_idx, fpw_idx


# offset 좌표 반환
def calculate_offset_point(vector: float, point_a: Vector3, offset_distance: float) -> Vector3:
    if offset_distance > 0:  # 우측 오프셋
        vector -= 90
    else:
        vector += 90  # 좌측 오프셋
    offset_a_xy = calculate_destination_coordinates(point_a.x, point_a.y, vector, abs(offset_distance))
    return Vector3(offset_a_xy[0], offset_a_xy[1], point_a.z)


def change_permile_to_degree(permile: float) -> float:
    """퍼밀 값을 도(degree)로 변환"""
    # 정수 또는 문자열이 들어오면 float으로 변환
    if not isinstance(permile, (int, float)):
        permile = float(permile)

    return math.degrees(math.atan(permile / 1000))  # 퍼밀을 비율로 변환 후 계산


def calculate_slope(h1: float, h2: float, gauge: float) -> float:
    """주어진 높이 차이와 수평 거리를 바탕으로 기울기(각도) 계산"""
    slope = (h2 - h1) / gauge  # 기울기 값 (비율)
    return math.degrees(math.atan(slope))  # 아크탄젠트 적용 후 degree 변환


class Direction(Enum):
    LEFT = -1
    RIGHT = 1
