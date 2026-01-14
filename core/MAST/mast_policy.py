from config.catalog.mast.mast_catalog import MastCatalog
from core.MAST.mast_rule import MastRuleSet
from core.MAST.mast_spec import MastSpec

class MastPolicy:
    def decide(self, ref, pole, speed) -> list[MastSpec]:
        material_code = MastRuleSet.select_code(speed, ref.structure_type)
        mast = MastCatalog.get(material_code)
        return [MastSpec(
            index=material_code,
            direction=pole.direction,
            name=MastCatalog.get_display_name(mast)
        )]