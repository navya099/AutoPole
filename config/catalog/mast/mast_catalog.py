from config.catalog.mast import MastMaterial
from pipe import PIPE_MASTS
from hbeam import HBEAM_MASTS
from utils.util import to_inch


class MastCatalog:
    PIPE = PIPE_MASTS
    HBEAM = HBEAM_MASTS

    @staticmethod
    def get(code: int) -> MastMaterial:
        return (
            MastCatalog.PIPE.get(code)
            or MastCatalog.HBEAM.get(code)
        )

    @staticmethod
    def get_display_name(mast: MastMaterial) -> str:
        if mast.type == "pipe":
            return MastCatalog.get_pipe_full_name(mast.diameter, mast.length)
        if mast.type == "h-beam":
            return MastCatalog.get_hbeam_full_name(mast.width, mast.height)
        return mast.name

    @staticmethod
    def get_pipe_full_name(diameter: float, length: float, thickness: float = 7.0) -> str:
        inch = to_inch(diameter)
        if inch is None:
            raise ValueError(f"미등록 직경: {diameter}")

        return f'P-{int(inch)}"x{int(thickness)}t-{length}m'

    @staticmethod
    def get_hbeam_full_name(width: float, height: float) -> str:
        return f'H형주-{width}X{height}'