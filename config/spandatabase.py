from types import MappingProxyType
from fileio.jsonloader import ConfigManager
import os
from utils.logger import logger
import glob

INVALID_SPAN_INDEX = 999_999_999
INVALID_OFFSET = (float("nan"), float("nan"))
INVALID_LIST = []

class SpanDatabase:
    """
    급전선 관련 데이터를 제공하는 클래스.
    주어진 데이터 딕셔너리를 읽기 전용으로 래핑하여 다양한 정보(설계 속도, 와이어 타입, 오프셋, 스팬 인덱스 등)를 반환한다.
    """

    def __init__(self ,speed: int):
        """
        SpanDatabase 객체 초기화
        """
        config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')

        files = glob.glob(os.path.join(config_dir, '**', f'cako{speed}.json'), recursive=True)
        if not files:
            raise FileNotFoundError(f"No config file for speed {speed} found")
        config_path = files[0]  # 첫 번째 발견된 파일 사용

        configmanager = ConfigManager(config_path)
        spandata = configmanager.config
        self._data = MappingProxyType(spandata)

    def get_span_index(self, structure: str, wire_type: str, span_length: int) -> int:
        """
        해당 조건에 맞는 스팬 인덱스를 반환
        :param structure: 구조물 타입 (예: "토공", "교량", "터널")
        :param wire_type: 와이어 타입
        :param span_length: 경간 길이 (단위: m)
        :return: 스팬 인덱스
        """
        try:
            return self._data[structure][wire_type]["span_index"][str(span_length)]
        except KeyError:

            logger.error(
                f"[SPAN_DB] Invalid span index: "
                f"structure={structure}, "
                f"wire={wire_type}, span={span_length}"
            )
            return INVALID_SPAN_INDEX


    def get_offset(self, wire_type: str, structure_type: str) -> tuple[float, float]:
        """
        해당 조건에 맞는 오프셋 좌표를 반환
        :param wire_type: 와이어 타입
        :param structure_type: 구조물 타입
        :return: (좌측, 우측) 오프셋 튜플. 존재하지 않을 경우 INVALID_OFFSET 예외
        """
        try:
            x =self._data[structure_type][wire_type]["offset"]["x"]
            y =self._data[structure_type][wire_type]["offset"]["y"]
            return float(x), float(y)
        except KeyError:
            logger.error(
                f"[SPAN_DB] Missing offset: "
                f"structure={structure_type}, "
                f"wire={wire_type}"
            )
            return INVALID_OFFSET