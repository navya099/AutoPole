from core.WIRE.base_wire_builder import BaseWireBuilder
from core.WIRE.wire_policy import WirePolicy


class ContactWireBuilder(BaseWireBuilder):
    wire_type = "contact"

    def apply(self, *, wire, i, data, pos, next_pos,
              pos_coord, next_pos_coord, vector_pos,
              span, loader, spandata, interpolator):

        current_structure = data.poles[i].current_structure
        next_structure = data.poles[i + 1].current_structure

        current_bracket = data.poles[i].brackets
        next_bracket = data.poles[i + 1].brackets

        # ✔ 여기서 "브래킷 개수만큼 contact 생성"도 가능
        WirePolicy.apply_contact(
            wire,
            i=i,
            data=data,
            spandata=spandata,
            interpolator=interpolator,
            loader=loader,
            pos=pos,
            next_pos=next_pos,
            pos_coord=pos_coord,
            next_pos_coord=next_pos_coord,
            vector_pos=vector_pos,
            span=span,
            current_structure=current_structure,
            next_structure=next_structure
        )
