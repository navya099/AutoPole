from typing import Optional

from config.catalog.bracket.bracket_materail import BracketMaterial
from config.catalog.bracket.bracket_type_enum import BracketBaseType, BracketInstallType, BracketSpecialType, \
    BracketVariant
from config.catalog.bracket.cako150 import CAKO150
from config.catalog.bracket.cako250 import CAKO250
from config.catalog.bracket.cako350 import CAKO350


class BracketCatalog:
    def __init__(self):
        self._catalog: dict[int, BracketMaterial] = {}

        self._catalog.update(CAKO150)
        self._catalog.update(CAKO250)
        self._catalog.update(CAKO350)

        self._catalog150 = CAKO150
        self._catalog250 = CAKO250
        self._catalog350 = CAKO350

    def get(self, code: int) -> BracketMaterial:
        return self._catalog.get(code)

    def get_name(self, code: int) -> str:
        mat = self.get(code)
        if mat is None:
            raise KeyError(f"Bracket code not found: {code}")
        return mat.name

    def find(
            self,
            *,
            speed,
            base_type: Optional[BracketBaseType] = None,
            special_type: Optional[BracketSpecialType] = None,
            install_type: Optional[BracketInstallType] = None,
            variant: Optional[BracketVariant] = None,
            gauge: Optional[float] = None,
    ) -> list[BracketMaterial]:
        result: list[BracketMaterial] = []
        if speed == 150:
            catalog = self._catalog150
        elif speed == 250:
            catalog = self._catalog250
        elif speed == 350:
            catalog = self._catalog350
        else:
            raise RuntimeError(f"Invalid speed: {speed}")
        for mat in catalog.values():
            if base_type is not None and mat.base_type != base_type:
                continue
            if special_type is not None and mat.special_type != special_type:
                continue
            if install_type is not None and mat.install_type != install_type:
                continue
            if variant is not None and mat.variant != variant:
                continue
            if gauge is not None and mat.gauge != gauge:
                continue

            result.append(mat)

        return result

    def find_one(self, **kwargs) -> BracketMaterial:
        result = self.find(**kwargs)
        if not result:
            raise LookupError("No matching bracket")
        if len(result) > 1:
            raise LookupError("Multiple brackets matched")
        return result[0]
