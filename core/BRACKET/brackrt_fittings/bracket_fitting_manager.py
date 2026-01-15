from config.catalog.bracket.bracket_type_enum import BracketBaseType
from core.AIRJOINT.airjoint_messangerwire_fitting import AirJointMessengerWireFitting
from core.AIRJOINT.airjoint_steadyarm_fitting import AirJointSteadyArmFitting
from core.BRACKET.brackrt_fittings.messenger_wire_fittings import MessengerWireFitting
from core.BRACKET.brackrt_fittings.steady_arm import SteadyArmFitting
from core.BRACKET.brackrt_fittings.wire_fitting import WireFixedFitting


class BracketFittingManager:
    def __init__(self, design_context, clusters):
        self.context = design_context
        self.clusters = clusters

    def run(self, polecollection):
        speed = self.context.speed
        for pole in polecollection.iter_poles():
            pole.fittings.clear()
            for bracket in pole.brackets:
                for strategy in self._select_strategies(bracket):
                    placement = strategy.fit(pole, bracket, speed)
                    if placement:
                        pole.fittings.append(placement)

    def _select_strategies(self, bracket):
        strategies = []

        # ✅ AirJoint 전용 fitting 우선
        if bracket.airjoint:
            strategies.extend(self._select_airjoint_strategies(bracket))
            return strategies  # ← 일반 전략 차단 (중요)

        # ===== 기존 로직 =====
        if bracket.bracket_type in {BracketBaseType.I, BracketBaseType.O}:
            strategies.append(SteadyArmFitting())
        elif bracket.bracket_type == BracketBaseType.F:
            strategies.append(WireFixedFitting())

        strategies.append(MessengerWireFitting())
        return strategies

    def _select_airjoint_strategies(self, bracket):
        strategies = []
        #곡선당김금구
        strategies.append(AirJointSteadyArmFitting())
        #지지금구
        strategies.append(AirJointMessengerWireFitting())

        return strategies


