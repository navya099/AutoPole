from config.catalog.bracket.bracket_type_enum import BracketBaseType
from core.BRACKET.brackrt_fittings.messenger_wire_fittings import MessengerWireFitting
from core.BRACKET.brackrt_fittings.steady_arm import SteadyArmFitting
from core.BRACKET.brackrt_fittings.wire_fitting import WireFixedFitting


class BracketFittingManager:
    def run(self, polecollection):
        for pole in polecollection.iter_poles():
            pole.fittings.clear()
            for bracket in pole.brackets:
                for strategy in self._select_strategies(bracket):
                    placement = strategy.fit(pole, bracket)
                    if placement:
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

