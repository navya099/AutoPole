from config.catalog.insulator.insulator import INSULATOR
from config.catalog.insulator.insulator_material import InsulatorMaterial


class InsulatorCatalog:
    _catalog = INSULATOR

    @classmethod
    def get(cls, code: int) -> InsulatorMaterial:
        mat = cls._catalog.get(code)
        if mat is None:
            raise KeyError(f"Insulator code not found: {code}")
        return mat

    @classmethod
    def find(cls, *, type: str = None, material: str = None) -> list[InsulatorMaterial]:
        result = []
        for mat in cls._catalog.values():
            if type is not None and mat.type != type:
                continue
            if material is not None and mat.material != material:
                continue
            result.append(mat)
        return result
