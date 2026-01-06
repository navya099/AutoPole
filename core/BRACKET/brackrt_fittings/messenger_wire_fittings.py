from core.BRACKET.brackrt_fittings.bracket_fitting_strategy import BracketFittingStrategy
from core.BRACKET.brackrt_fittings.fitting_type_enum import FittingTypeEnum
from core.BRACKET.brackrt_fittings.messenger_wire_placement import MessengerWirePlacement
from utils.util import TrackSide


class MessengerWireFitting(BracketFittingStrategy):
    """조가선 지지 금구 설치 전략"""

    def fit(self, pole, bracket_spec):
        # 조가선은 브래킷 타입과 무관하게 설치
        stagger = self.calc_stagger(bracket_spec)

        return MessengerWirePlacement(
            pole_pos=pole.pos,
            bracket_index=bracket_spec.index,
            code=0,   # catalog 연동 가능
            stagger=stagger,
            side=TrackSide.Inner,
            type=FittingTypeEnum.Messenger,
        )

    def calc_stagger(self, bracket_spec):
        # 필요 없으면 0.0으로 고정도 가능
        return 0.0
