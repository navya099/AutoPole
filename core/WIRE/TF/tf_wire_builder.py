from core.POLE.polegroup_collector import PoleGroupCollection
from core.WIRE.base_wire_builder import BaseWireBuilder
from utils.Vector3 import Vector3


class TFWireBuilder(BaseWireBuilder):
    wire_type: str

    def apply(
        self,
        *,
        wire,
        i: int,
        data: PoleGroupCollection,
        pos: float,
        next_pos: float,
        pos_coord: Vector3,
        next_pos_coord: Vector3,
        vector_pos: float,
        span: float,
        loader,
        spandata,
        interpolator
    ):
        raise NotImplementedError
