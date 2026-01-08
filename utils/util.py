import math
import uuid
from enum import Enum

from utils.logger import logger
from typing import Literal, List, Tuple
from utils.Vector3 import Vector3

def generate_entity_id() -> int:
    """8자리 수준의 고유 ID 생성"""
    return uuid.uuid4().int & 0xFFFFFFFF  # 하위 32비트만 사용

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





def buffered_write(filename, lines):
    """파일 쓰기 버퍼 함수"""
    filename = "C:/TEMP/" + filename
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)







def calculate_bearing(x1: float, y1: float, x2: float, y2: float) -> float:
    # Calculate the bearing (direction) between two points in Cartesian coordinates
    dx = x2 - x1
    dy = y2 - y1
    bearing = math.atan2(dy, dx)
    return bearing


def calculate_destination_coordinates(x1: float, y1: float, bearing: float, distance: float) -> tuple[float, float]:
    # Calculate the destination coordinates given a starting point, bearing, and distance in Cartesian coordinates
    angle = bearing
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

    def opposite(self):
        return Direction.RIGHT if self is Direction.LEFT else Direction.LEFT

def to_inch(number: float) -> float:
    return number / 25.4

class TrackSide(Enum):

    Inner = 0
    Outer = 1
    NONE = 2
