import re
import math
from .logger import logger
from typing import Literal


def validate_structure_list(structure_list: dict) -> bool:
    """
    입력 딕셔너리 리스트를 검증하는 유틸함수
    :param structure_list:
    :return: bool
    """
    if not isinstance(structure_list, dict):
        raise TypeError("structure_list must be a dictionary.")

    for key in ['bridge', 'tunnel']:
        if key in structure_list:
            value = structure_list[key]
            if not isinstance(value, list):
                raise TypeError(f"'{key}' must be a list of (start, end) tuples.")

            for i, item in enumerate(value):
                if not (isinstance(item, tuple) and len(item) == 2):
                    raise TypeError(f"Item at index {i} in '{key}' must be a tuple with two elements.")

                start, end = item
                if not (isinstance(start, (int, float)) and isinstance(end, (int, float))):
                    raise TypeError(f"Start and end values in '{key}[{i}]' must be int or float.")
        return True


def isbridge_tunnel(sta: float, structure_list: dict) -> Literal['교량', '터널', '토공']:
    """
    주어진 위치 sta가 교량, 터널, 또는 기본적으로 토공인지 판별하는 함수.

    :param int sta: 위치 (거리값)
    :param structure_list: dict {'bridge': [(start, end)], 'tunnel': [(start, end)]}
    :return: str:'교량', '터널', 또는 '토공' 실패시에도 '토공' 반환
    """
    ...
    try:
        validate_structure_list(structure_list)

        for start, end in structure_list.get('bridge', []):
            if start <= sta <= end:
                return '교량'

        for start, end in structure_list.get('tunnel', []):
            if start <= sta <= end:
                return '터널'

    except Exception as ex:
        logger.error(
            f"🚨 structure_list validation failed: {type(ex).__name__} - {ex} | sta={sta}")

    return '토공'


def check_isairjoint(input_sta, airjoint_list):
    for data in airjoint_list:
        sta, tag = data
        if input_sta == sta:
            return tag
    return '일반개소'


def get_block_index(current_track_position, block_interval=25):
    """현재 트랙 위치를 블록 인덱스로 변환"""
    return math.floor(current_track_position / block_interval + 0.001) * block_interval


def iscurve(cur_sta, curve_list):
    """sta가 곡선 구간에 해당하는지 구분하는 함수"""
    rounded_sta = get_block_index(cur_sta)  # 25 단위로 반올림

    for sta, R, c in curve_list:
        if rounded_sta == sta:
            if R == 0:
                return '직선', 0, 0  # 반경이 0이면 직선
            return '곡선', R, c  # 반경이 존재하면 곡선

    return '직선', 0, 0  # 목록에 없으면 기본적으로 직선 처리


def isslope(cur_sta, curve_list):
    """sta가 곡선 구간에 해당하는지 구분하는 함수"""
    rounded_sta = get_block_index(cur_sta)  # 25 단위로 반올림

    for sta, g in curve_list:
        if rounded_sta == sta:
            if g == 0:
                return '수평', 0  # 반경이 0이면 직선
            else:
                return '기울기', f'{g * 1000:.2f}'

    return '수평', 0  # 목록에 없으면 기본적으로 직선 처리


def find_last_block(data: list[str]) -> int:
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


def get_elevation_pos(pos, polyline_with_sta):
    new_z = None

    for i in range(len(polyline_with_sta) - 1):
        sta1, x1, y1, z1 = polyline_with_sta[i]  # 현재값
        sta2, x2, y2, z2 = polyline_with_sta[i + 1]  # 다음값
        length = sta2 - sta1
        length_new = pos - sta1

        if sta1 <= pos < sta2:
            new_z = calculate_height_at_new_distance(z1, z2, length, length_new)
            return new_z

    return new_z


def calculate_height_at_new_distance(h1, h2, length, length_new):
    """주어진 거리 L에서의 높이 변화율을 기반으로 새로운 거리 L_new에서의 높이를 계산"""
    h3 = h1 + ((h2 - h1) / length) * length_new
    return h3


def return_pos_coord(polyline_with_sta, pos):
    point_a, _, vector_a = interpolate_coordinates(polyline_with_sta, pos)
    return point_a, vector_a


def interpolate_coordinates(
        polyline: list[tuple[int, float, float, float]], target_sta: int) -> \
        tuple[tuple[float, float, float], tuple[float, float, float], float]:
    """
    주어진 폴리선 데이터에서 특정 sta 값에 대한 좌표를 선형 보간하여 반환.

    :param polyline: [(sta, x, y, z), ...] 형식의 리스트
    :param target_sta: 찾고자 하는 sta 값
    :return: (x, y, z) 좌표 튜플
    """
    # 정렬된 리스트를 가정하고, 적절한 두 점을 찾아 선형 보간 수행
    for i in range(len(polyline) - 1):
        sta1, x1, y1, z1 = polyline[i]
        sta2, x2, y2, z2 = polyline[i + 1]
        v1 = calculate_bearing(x1, y1, x2, y2)
        # target_sta가 두 점 사이에 있는 경우 보간 수행
        if sta1 <= target_sta < sta2:
            t = abs(target_sta - sta1)
            x, y = calculate_destination_coordinates(x1, y1, v1, t)
            z = calculate_height(z1, z2, sta2 - sta1, t)
            interpolate_coord = (x, y, z)
            origin_coord = (x1, y1, z1)
            return interpolate_coord, origin_coord, v1


def calculate_height(z1, z2, length, horizontal_distance):
    # 높이 차이
    delta_z = z2 - z1

    # 경사면 전체 길이에 대한 경사율
    slope = delta_z / length

    # 수평 거리만큼 진행했을 때 높이 변화량
    delta_z_x = slope * horizontal_distance

    # 최종 높이
    z = z1 + delta_z_x
    return z


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


def calculate_curve_angle(
        polyline_with_sta: list[tuple[int, float, float, float]],
        pos: int, next_pos: int, stagger1: float, stagger2: float) -> float:
    """
    전차선의 좌우 offset을 고려한 yaw 각도 계산 함수
    :param polyline_with_sta: 선형 좌표 리스트
    :param pos: 시작 측점
    :param next_pos: 끝 측점
    :param stagger1: 시작점 좌우 offset
    :param stagger2: 끝점 좌우 offset
    :return: yaw angle (degrees)
    """
    final_anlge = 0.0  # 변수초기화

    # 시작pos와 끝 pos의 좌표와 폴리선 벡터 반환
    point_a, _, vector_a = interpolate_coordinates(polyline_with_sta, pos)
    point_b, _, vector_b = interpolate_coordinates(polyline_with_sta, next_pos)

    if point_a and point_b:
        # offset 점 계산
        offset_point_a = calculate_offset_point(vector_a, point_a, stagger1)
        offset_point_b = calculate_offset_point(vector_b, point_b, stagger2)

        # offset점끼리의 각도
        a_b_angle = calculate_bearing(offset_point_a[0], offset_point_a[1], offset_point_b[0], offset_point_b[1])

        # 최종 각도
        final_anlge = vector_a - a_b_angle
    return final_anlge


# offset 좌표 반환
def calculate_offset_point(vector: float, point_a: tuple[float, float, float], offset_distance: float) -> \
        tuple[float, float]:
    if offset_distance > 0:  # 우측 오프셋
        vector -= 90
    else:
        vector += 90  # 좌측 오프셋
    offset_a_xy = calculate_destination_coordinates(point_a[0], point_a[1], vector, abs(offset_distance))
    return offset_a_xy


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
