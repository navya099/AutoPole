from dataclasses import dataclass

from core.BRACKET.brackrt_fittings.fitting_type_enum import FittingTypeEnum
from utils.util import TrackSide

@dataclass
class BaseFittingPlace:
    pole_pos: int
    bracket_index: int
    side: TrackSide
    code: int
    stagger: float
    type: FittingTypeEnum