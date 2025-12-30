from utils.Vector3 import Vector3
from geometryor.alignment import BVEAlignment
from utils.logger import logger
from utils.util import calculate_bearing, calculate_destination_coordinates, calculate_offset_point


class CoordinateInterpolator:
    """폴리선 보간 기능을 수행하는 유틸클래스
        Attributes:
            bvealignment (BVEAlignment): bve선형객체
            interpolate_coord (Vector3): 보간된 점의 좌표 Vector3
            origin_coord (Vector3): 보간된 점의 시작점 좌표 Vector3
            vector (float): 시작점의 방향벡터(각도)
    """
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
