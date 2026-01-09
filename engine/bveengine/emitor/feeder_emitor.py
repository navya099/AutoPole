from core.bve_element import BVEFreeobj
from engine.interface.railwatir import RailwayIR


class FeederEmitter:
    def emit(self, ir: RailwayIR) -> BVEFreeobj:
        obj = BVEFreeobj()
        obj.name = ir.name
        obj.object_index = ir.code
        obj.rail_index = ir.track

        obj.yaw = 180 if ir.meta.get("is_flipped") else 0
        obj.position_x = 0
        obj.position_y = 0
        obj.pitch = 0
        obj.roll = 0
        return obj
