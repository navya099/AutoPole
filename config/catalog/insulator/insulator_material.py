from dataclasses import dataclass


@dataclass
class InsulatorMaterial:
    name: str
    code: int
    type: str
    material: str
