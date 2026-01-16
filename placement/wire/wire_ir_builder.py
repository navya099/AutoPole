from config.spandatabase import SpanDatabase
from core.WIRE.wire_bundle import WireBundle
from engine.interface.ircalculaotor import IRCalculator
from engine.interface.railwatir import RailwayIR
from geometryor.wiregeometry import WireGeometry
from placement.wire.wire_placement_resolver import WirePlacementResolver


class WireIRBuilder:
    def __init__(self, span_db: SpanDatabase, pole_lookup):
        self.resolver = WirePlacementResolver(span_db)
        self.calculator = IRCalculator()
        self.pole_lookup = pole_lookup

    def build(self, bundle: WireBundle) -> list[RailwayIR]:
        irs = []
        track_index = bundle.track_index
        start_pole = self.pole_lookup.get_by_ref(bundle.start_ref, track_index)
        end_pole = self.pole_lookup.get_by_ref(bundle.end_ref, track_index)

        if not start_pole or not end_pole:
            return irs

        for wire in bundle.wires:
            placement = self.resolver.resolve(bundle.start_ref, wire.type)
            st = self.calculator.calc_offset_position_xy(
                start_pole,
                placement.offset_x,
                placement.offset_y
            )
            ed = self.calculator.calc_offset_position_xy(
                end_pole,
                placement.offset_x,
                placement.offset_y
            )
            irs.append(RailwayIR(
                station=bundle.start_ref.pos,
                category="wire",
                code=placement.index,
                track=track_index,
                geometry=WireGeometry(start=st, end=ed),
                meta={"wire_type": wire.type,
                      "offset_x":placement.offset_x,
                      "offset_y":placement.offset_y,
                      },
                position=None,
                direction=None
            ))
        return irs


