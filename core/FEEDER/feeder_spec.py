from dataclasses import dataclass

from utils.util import Direction


@dataclass
class FeederSpec:
    index: int
    name: str
    direction: Direction
    offset: float
