from dataclasses import dataclass

from utils.util import Direction


@dataclass
class MastSpec:
    index: int
    direction: Direction
