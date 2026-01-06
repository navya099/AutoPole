from dataclasses import dataclass
from core.WIRE.wire_type import WireType
from core.section.section_type import SectionType


@dataclass(frozen=True)
class WirePolicy:
    min_count: int
    max_count: int

    def decide(self, start_ref, end_ref) -> int:
        # 기본: 고정 개수
        if self.min_count == self.max_count:
            return self.min_count

        # CONTACT 전선 특수 규칙 예시
        if start_ref.structure_type == "ISLAND_PLATFORM":
            return self.max_count

        return self.min_count

WIRE_POLICY_TABLE = {
    SectionType.NORMAL: {
        WireType.FPW: WirePolicy(1, 1),
        WireType.AF: WirePolicy(1, 1),
        WireType.CONTACT: WirePolicy(1, 1),
    },
    SectionType.AIRJOINT: {
        WireType.FPW: WirePolicy(1, 1),
        WireType.AF: WirePolicy(1, 1),
        WireType.CONTACT: WirePolicy(1, 2),
    },
    SectionType.SUBSTATION: {
        WireType.FPW: WirePolicy(1, 1),
        WireType.AF: WirePolicy(1, 1),
        WireType.TF: WirePolicy(1, 1),
        WireType.CONTACT: WirePolicy(1, 2),
    },
    SectionType.STATION: {
        WireType.FPW: WirePolicy(1, 2),
        WireType.AF: WirePolicy(1, 2),
        WireType.CONTACT: WirePolicy(1, 3),
    },
}
