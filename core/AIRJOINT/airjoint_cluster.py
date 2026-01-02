from dataclasses import dataclass

from core.POLE.poledata import PolePlaceDATA


@dataclass
class AirJointCluster:
    number: str
    positions: list[int]  # 반드시 5개
