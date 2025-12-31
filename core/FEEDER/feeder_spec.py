from dataclasses import dataclass

from utils.util import Direction


@dataclass
class FeederSpec:
    type: str
    index: int
    name: str
    direction: Direction
