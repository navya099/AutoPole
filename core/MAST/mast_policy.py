from core.MAST.mast_rule import MastRuleSet
from core.MAST.mast_spec import MastSpec

class MastPolicy:
    def decide(self, ref, pole, speed) -> list[MastSpec]:
        material_code = MastRuleSet.select_code(speed, ref.structure_type)
        return [MastSpec(
            index=material_code,
            direction=pole.direction
        )]