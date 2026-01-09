from core.bve_element import BVEFreeobj
from engine.interface.railwatir import RailwayIR


class WireEmitter:
    def emit(self, ir: RailwayIR) -> BVEFreeobj:
        obj = BVEFreeobj()
        obj.name = ir.name
        obj.object_index = ir.code
        obj.rail_index = ir.track

        obj.yaw = ir.geometry.plan_anlge
        obj.position_x = ir.meta.get("offset_x",0.0)
        obj.position_y = ir.meta.get("offset_y",0.0)
        obj.pitch = ir.geometry.slope_angle
        obj.roll = 0.0
        return obj
