from config.catalog.bracket.bracket_type_enum import BracketBaseType
from core.BRACKET.brackrt_fittings.messenger_wire_fittings import MessengerWireFitting
from core.BRACKET.brackrt_fittings.steady_arm import SteadyArmFitting
from core.BRACKET.brackrt_fittings.wire_fitting import WireFixedFitting


class BracketFittingManager:
    def run(self, polecollection):
        for group_index, group in enumerate(polecollection):
            for pole in group:
                for bracket in pole.brackets:
                    strategies = self._select_strategies(bracket)
                    for strategy in strategies:
                        placement = strategy.fit(pole, bracket)
                        if placement is not None:
                            pole.fittings.append(placement)

    def _select_strategies(self, bracket):
        strategies = []

        # 타입별
        if bracket.bracket_type in {BracketBaseType.I, BracketBaseType.O}:
            strategies.append(SteadyArmFitting())
        elif bracket.bracket_type == BracketBaseType.F:
            strategies.append(WireFixedFitting())

        # 공통
        strategies.append(MessengerWireFitting())

        return strategies

