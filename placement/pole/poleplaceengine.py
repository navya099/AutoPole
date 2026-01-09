from core.POLE.poledata import PolePlaceDATA
from engine.interface.ircalculaotor import IRCalculator
from engine.interface.railwatir import RailwayIR
from utils.util import Direction

class PolePlaceIRBuilder:
    def __init__(self):
        self.calculator = IRCalculator()

    def build(self, pole: PolePlaceDATA) -> list[RailwayIR]:
        irs: list[RailwayIR] = []

        track = pole.track_index
        direction = pole.direction
        base = pole.ref.center_coord #선형중심좌표

        # Mast
        for mast in pole.masts:
            irs.append(RailwayIR(
                category="mast",
                code=mast.code,
                track=track,
                position=pole.coord,
                direction=mast.direction,
                meta={"section": pole.current_section,
                      "gauge": pole.gauge}
            ))

        # Bracket
        for br in pole.brackets:
            is_flipped = br.direction != Direction.RIGHT

            irs.append(RailwayIR(
                category="bracket",
                code=br.index,
                track=track,
                position=base,
                direction=br.direction,
                name=br.name,
                meta={
                    "gauge": pole.gauge,
                    "ispreader": pole.ispreader,
                    "is_flipped": is_flipped
                }
            ))

        # Feeder
        for feeder in pole.feeders:
            is_flipped = feeder.direction != Direction.RIGHT
            irs.append(RailwayIR(
                category="feeder",
                code=feeder.code,
                track=track,
                position=pole.coord,
                direction=feeder.direction,
                name=feeder.name,
                meta = {
                    "is_flipped": is_flipped
                }
            ))

        # Fittings (금구류)
        for fitting in pole.fittings:
            position = pole.coord.copy()
            apply_position = self.calculator.calc_offset_position(pole, fitting.stagger)
            irs.append(RailwayIR(
                category="fitting",
                code=fitting.code,
                track=track,
                position=apply_position,   # 필요 시 offset 적용
                direction=direction,
                meta={
                    "stagger": fitting.stagger,
                } # ← fitting 객체 책임
            ))

        return irs
