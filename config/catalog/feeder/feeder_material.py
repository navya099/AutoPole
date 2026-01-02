from dataclasses import dataclass

from config.catalog.feeder.crossarm_material import CrossarmMaterial
from config.catalog.insulator.insulator_material import InsulatorMaterial


@dataclass(frozen=True)
class FeederMaterial:
    crossarms: list[CrossarmMaterial]
    insulators: list[InsulatorMaterial]
    lines: int
    code: int
    name: str