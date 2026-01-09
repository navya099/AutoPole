from dataclasses import dataclass


@dataclass(frozen=True)
class WirePlacement:
    index: int
    offset_x: float
    offset_y: float
