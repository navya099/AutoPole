from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AirJointState:
    airjoint_id: str          # AJ-1
    cluster_index: int        # 0~4 (전주 위치)
    bracket_order: int        # 해당 전주 내 순서
