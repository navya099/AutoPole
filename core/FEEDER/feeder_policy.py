from config.catalog.feeder.feeder_catalog import FeederCatalog
from core.FEEDER.feeder_spec import FeederSpec


class FeederPolicy:
    def __init__(self):
        self.map = {
            ('토공', 150): 1234,
            ('토공', 250): 1234,
            ('토공', 350): 597,
            ('교량', 150): 1234,
            ('교량', 250): 1234,
            ('교량', 350): 597,
            ('터널', 150): 1249,
            ('터널', 250): 1249,
            ('터널', 350): 598,
        }

    def decide(self, pole, speed) -> list[FeederSpec]:
        specs: list[FeederSpec] = []

        # 기본 단일 급전선
        base = self.decide_single(pole, speed)
        specs.append(base)

        #장래 확장 가능
        """기본AF+보조급전선TF가 달린 전주"""
        return specs

    def decide_single(self, pole, speed):
        index = self.map.get(
            (pole.ref.structure_type, speed),
            1234
        )
        mat = FeederCatalog.get(index)
        return FeederSpec(
            type = 'AF',
            index=index,
            name=mat.name,
            direction=pole.direction,
        )
