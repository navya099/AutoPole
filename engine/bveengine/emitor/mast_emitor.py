from core.bve_element import BVEFreeobj
from engine.interface.railwatir import RailwayIR
from utils.util import Direction

class MastEmitter:
    def emit(self, ir: RailwayIR) -> BVEFreeobj:
        obj = BVEFreeobj()
        obj.name = ir.name
        obj.object_index = ir.code
        obj.rail_index = ir.track
        if "gauge" not in ir.meta:
            raise ValueError("Mast IR requires 'gauge'")
        gauge = ir.meta.get("gauge", 0.0)
        obj.position_x = -gauge if ir.direction == Direction.LEFT else gauge
        obj.position_y = 0
        obj.yaw = 0
        obj.pitch = 0
        obj.roll = 0
        return obj
