from core.WIRE.wire_bundle import WireBundle
from core.WIRE.wire_element import WireElement
from core.WIRE.wire_type import WireType
from collections import defaultdict

class WireDataManager:
    """
    전체 전선 네트워크를 관리하는 컨테이너 클래스
    (순수 데이터 구조)
    """

    def __init__(self):
        self.bundles: list[WireBundle] = []

    # ---------- 기본 관리 ----------

    def add_bundle(self, bundle: WireBundle):
        self.bundles.append(bundle)

    def is_empty(self) -> bool:
        return len(self.bundles) == 0

    # ---------- 조회 유틸 ----------

    def iter_bundles(self):
        yield from self.bundles

    def iter_wires(self):
        """모든 WireElement 순회"""
        for bundle in self.bundles:
            for wire in bundle.wires:
                yield wire

    def get_bundles_by_wire_type(self, wire_type: WireType) -> list[WireBundle]:
        return [
            bundle for bundle in self.bundles
            if bundle.has_wire(wire_type)
        ]

    def get_wires_by_type(self, wire_type: WireType) -> list[WireElement]:
        result = []
        for bundle in self.bundles:
            result.extend(bundle.get_wires(wire_type))
        return result

    # ---------- 디버깅 / 검사 ----------

    def summary(self) -> dict:
        """
        전선 종류별 개수 요약
        """

        counter = defaultdict(int)
        for wire in self.iter_wires():
            counter[wire.type] += 1
        return dict(counter)
