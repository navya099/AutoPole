from typing import List, Optional
from config.catalog.feeder.feeder import FEEDER
from config.catalog.feeder.feeder_material import FeederMaterial

class FeederCatalog:
    _catalog = FEEDER

    @classmethod
    def get(cls, code: int) -> FeederMaterial:
        mat = cls._catalog.get(code)
        if mat is None:
            raise KeyError(f"Feeder code not found: {code}")
        return mat

    @classmethod
    def find(
        cls,
        *,
        lines: Optional[int] = None,
        special: Optional[bool] = None
    ) -> List[FeederMaterial]:
        """조건 기반 검색"""
        result: List[FeederMaterial] = []
        for mat in cls._catalog.values():
            if lines is not None and mat.lines != lines:
                continue
            if special is not None and mat.special != special:
                continue
            result.append(mat)
        return result

    @classmethod
    def find_one(
        cls,
        *,
        lines: Optional[int] = None,
        special: Optional[bool] = None
    ) -> FeederMaterial:
        """조건 기반 검색, 하나만 반환"""
        mats = cls.find(lines=lines, special=special)
        if not mats:
            raise RuntimeError("No feeder matching the conditions.")
        return mats[0]
