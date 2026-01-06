from config.catalog.bracket.bracket_type_enum import BracketBaseType
from core.BRACKET.brackrt_fittings.bracket_fitting_strategy import BracketFittingStrategy
from core.BRACKET.brackrt_fittings.fitting_type_enum import FittingTypeEnum
from core.BRACKET.brackrt_fittings.steady_arm_placer import SteadyArmPlacement
from utils.util import TrackSide


class SteadyArmFitting(BracketFittingStrategy):
    def fit(self, pole, bracket_spec):

        #표준 피팅
        stagger = self.fit_stagger(bracket_spec)
        arm_install_direction = self.define_arm_install_direction(bracket_spec)
        return SteadyArmPlacement(
            pole_pos=pole.pos,
            bracket_index=bracket_spec.index,
            side=arm_install_direction,
            code=0,#임시
            stagger=stagger,
            type=FittingTypeEnum.SteadyArm
        )

    def fit_stagger(self, bracket_spec):
        if bracket_spec.bracket_type == BracketBaseType.I:
            stagger = -0.2
        elif bracket_spec.bracket_type == BracketBaseType.O:
            stagger = 0.2
        elif bracket_spec.bracket_type == BracketBaseType.F:
            stagger = 0.35
        else:
            raise ValueError(bracket_spec.bracket_type)
        return stagger

    def define_arm_install_direction(self, bracket_spec):
        if bracket_spec.bracket_type == BracketBaseType.I:
            return TrackSide.Inner
        elif bracket_spec.bracket_type == BracketBaseType.O:
            return TrackSide.Outer
        elif bracket_spec.bracket_type == BracketBaseType.F:
            return TrackSide.NONE
        else:
            raise ValueError(bracket_spec.bracket_type)
