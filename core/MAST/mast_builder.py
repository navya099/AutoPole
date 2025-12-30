from core.MAST.mast_policy import MastPolicy
from core.POLE.poledata import PolePlaceDATA


class MastBuilder:
    def __init__(self, policy: MastPolicy):
        self.policy = policy

    def apply(self, pole: PolePlaceDATA, speed):
        specs = self.policy.decide(pole.ref, pole, speed)
        pole.apply_mast(specs)
