from config.catalog.fittings.bracket_fittings import FittingCatalog
from config.catalog.fittings.fitting_role import FittingRole
from core.BRACKET.brackrt_fittings.bracket_fitting_strategy import BracketFittingStrategy
from core.BRACKET.brackrt_fittings.fitting_type_enum import FittingTypeEnum
from core.BRACKET.brackrt_fittings.messenger_wire_placement import MessengerWirePlacement
from core.BRACKET.brackrt_fittings.steady_arm import SteadyArmFitting
from utils.util import TrackSide


class MessengerWireFitting(SteadyArmFitting):
    """조가선 지지 금구 설치 전략"""

    def fit(self, pole, bracket_spec, speed):
        # 조가선은 브래킷 타입과 무관하게 설치
        stagger = self.fit_standard_stagger(bracket_spec)
        mat = FittingCatalog.get(speed, FittingRole.NORMAL_MESSENGER)
        return MessengerWirePlacement(
            pole_pos=pole.pos,
            bracket_index=bracket_spec.index,
            code=mat.code,   # catalog 연동 가능
            stagger=stagger,
            side=TrackSide.NONE,
            type=FittingTypeEnum.Messenger,
        )