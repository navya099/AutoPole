from config.spandatabase import SpanDatabase
from core.WIRE.wire_type import WireType
from placement.wire.wire_placement import WirePlacement
from config.spandatabase import INVALID_SPAN_INDEX, INVALID_OFFSET


class WirePlacementResolver:
    def __init__(self, span_db: SpanDatabase):
        self.span_db = span_db

    def resolve(self, pole_ref, wire_type: WireType) -> WirePlacement:
        structure = pole_ref.structure_type
        span = pole_ref.span

        index = self.span_db.get_span_index(structure, wire_type.name.lower(), span)
        if index == INVALID_SPAN_INDEX:
            raise ValueError(f"Span index not found for {structure} / {wire_type.name} / {span}")

        #✅ offset이 없는 wire
        if wire_type == WireType.CONTACT:
            return WirePlacement(index=index,offset_x=0, offset_y=0)
        offset_x, offset_y = self.span_db.get_offset(wire_type.name.lower(), structure)
        if (offset_x, offset_y) == INVALID_OFFSET:
            raise ValueError(f"Offset not found for {structure} / {wire_type.name}")

        return WirePlacement(
            index=index,
            offset_x=offset_x,
            offset_y=offset_y
        )
