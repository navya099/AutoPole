from config.catalog.fittings.bracket_fittings import FittingCatalog
from config.catalog.fittings.fitting_role import FittingRole
from core.AIRJOINT.airjoint_steadyarm_fitting import AirJointSteadyArmFitting
from core.BRACKET.brackrt_fittings.bracket_fitting_strategy import BracketFittingStrategy
from core.BRACKET.brackrt_fittings.fitting_type_enum import FittingTypeEnum
from core.BRACKET.brackrt_fittings.messenger_wire_placement import MessengerWirePlacement
from utils.util import TrackSide


class AirJointMessengerWireFitting(AirJointSteadyArmFitting):
    def fit(self, pole, bracket_spec, speed):
        # 에어조인트구간 조가선

        stagger = self.cal_stagger(bracket_spec)
        mat = FittingCatalog.get(speed, FittingRole.AIRJOINT_MESSENGER)
        return MessengerWirePlacement(
            pole_pos=pole.pos,
            bracket_index=bracket_spec.index,
            code=mat.code,  # catalog 연동 가능
            stagger=stagger,
            side=TrackSide.NONE,
            type=FittingTypeEnum.Messenger,
        )
