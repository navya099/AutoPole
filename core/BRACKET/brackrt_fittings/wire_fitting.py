from core.BRACKET.brackrt_fittings.bracket_fitting_strategy import BracketFittingStrategy
from core.BRACKET.brackrt_fittings.fitting_type_enum import FittingTypeEnum
from core.BRACKET.brackrt_fittings.wire_fixed_place import WireFixedPlacement
from utils.util import TrackSide


class WireFixedFitting(BracketFittingStrategy):
    def fit(self, pole, bracket_spec):
        return WireFixedPlacement(
            pole_pos=pole.pos,
            bracket_index=bracket_spec.index,
            side=TrackSide.NONE,
            code=0,
            stagger=0,
            type= FittingTypeEnum.Clamp
        )
