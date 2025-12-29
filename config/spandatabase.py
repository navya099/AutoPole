from types import MappingProxyType
from fileio.jsonloader import ConfigManager
import os

class SpanDatabase:
    """
    급전선 관련 데이터를 제공하는 클래스.
    주어진 데이터 딕셔너리를 읽기 전용으로 래핑하여 다양한 정보(설계 속도, 와이어 타입, 오프셋, 스팬 인덱스 등)를 반환한다.
    """

    def __init__(self):
        """
        SpanDatabase 객체 초기화
        """
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'span_data.json')
        configmanager = ConfigManager(config_path)
        spandata = configmanager.config
        self._data = MappingProxyType(spandata)

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