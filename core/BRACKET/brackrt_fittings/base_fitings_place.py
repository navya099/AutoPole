from dataclasses import dataclass
from utils.util import TrackSide

@dataclass
class BaseFittingPlace:
    pole_pos: int
    bracket_index: int
    side: TrackSide
    code: int
    stagger: float