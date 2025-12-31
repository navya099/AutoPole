from dataclasses import dataclass

from core.POLE.poledata import PolePlaceDATA


@dataclass
class AirJointCluster:
    poles: list[PolePlaceDATA]  # 반드시 5개
