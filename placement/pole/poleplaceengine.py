from core.POLE.poledata import PolePlaceDATA
from engine.interface.ircalculaotor import IRCalculator
from engine.interface.railwatir import RailwayIR
from utils.util import Direction, offsets
from collections import defaultdict

class PolePlaceIRBuilder:
    def __init__(self):
        self.calculator = IRCalculator()

    def build(self, pole: PolePlaceDATA) -> list[RailwayIR]:
        irs: list[RailwayIR] = []

        track = pole.track_index
        direction = pole.direction
        base = pole.ref.center_coord #선형중심좌표
        pos = pole.pos
        # Mast
        for mast in pole.masts:
            irs.append(RailwayIR(
                station=pos,
                category="mast",
                name=mast.name,
                code=mast.code,
                track=track,
                position=pole.coord,
                direction=mast.direction,
                meta={"section": pole.current_section,
                      "gauge": pole.gauge,
                      "postnumber": pole.post_number,
                      "curve": pole.ref.curve_type}
            ))

        # Bracket
        n = len(pole.brackets)
        s = 1
        offs = offsets(n, s)  # 🔥 한 번만 계산
        for i, br in enumerate(pole.brackets):
            is_flipped = pole.direction != Direction.LEFT

            irs.append(RailwayIR(
                station=pos + offs[i],
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
                station=pole.pos,
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

        bracket_code_to_slot = {
            br.index: i
            for i, br in enumerate(pole.brackets)
        }

        fittings_by_bracket_code = defaultdict(list)
        for fitting in pole.fittings:
            fittings_by_bracket_code[fitting.bracket_index].append(fitting)

        for br_code, slot in bracket_code_to_slot.items():
            station = pos + offs[slot]

            for fitting in fittings_by_bracket_code.get(br_code, []):
                apply_position = self.calculator.calc_offset_position(
                    pole, fitting.stagger
                )

                irs.append(RailwayIR(
                    station=station,
                    category="fittings",
                    name=fitting.type.name,
                    code=fitting.code,
                    track=track,
                    position=apply_position,
                    direction=direction,
                    meta={
                        "stagger": fitting.stagger,
                        "type": fitting.type,
                    }
                ))

        return irs
