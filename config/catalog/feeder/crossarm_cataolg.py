from config.catalog.feeder.crossarm import CROSSARM
from config.catalog.feeder.crossarm_material import CrossarmMaterial


class CrossarmCatalog:
    _catalog = CROSSARM

    @classmethod
    def get(cls, code: int) -> CrossarmMaterial:
        mat = cls._catalog.get(code)
        if mat is None:
            raise KeyError(f"Crossarm code not found: {code}")
        return mat
