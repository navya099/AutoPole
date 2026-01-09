from core.bve_element import BVEFreeobj
from engine.bveengine.emitor.bracket_emitor import BracketEmitter
from engine.bveengine.emitor.feeder_emitor import FeederEmitter
from engine.bveengine.emitor.fittin_emitor import BracketFittingsEmitter
from engine.bveengine.emitor.mast_emitor import MastEmitter
from engine.bveengine.emitor.wire_emitor import WireEmitter
from engine.interface.railwatir import RailwayIR
from engine.interface.serilalize_interfece import SerializationEngine


class BveEngine(SerializationEngine):

    def __init__(self):
        self.lines = []
        self.emitters = {
            "mast": MastEmitter(),
            "feeder": FeederEmitter(),
            "bracket": BracketEmitter(),
            "fitings" : BracketFittingsEmitter(),
            "wire": WireEmitter()
        }
    def begin(self):
        self.lines.append(",; BVE BEGIN")

    def emit(self, ir: RailwayIR):
        emitter = self.emitters.get(ir.category)
        if not emitter:
            raise ValueError(f"Unsupported IR category: {ir.category}")

        obj = emitter.emit(ir)
        self.lines.append(self.serialize(obj,comment=ir.category))

    def end(self):
        self.lines.append(",; BVE END")
        return "\n".join(self.lines)

    def serialize(self, obj: BVEFreeobj, comment: str = '') -> str:
        lines = []

        if comment:
            lines.append(f'.;{comment}')

        lines.append(
            f".freeobj {obj.position_x};{obj.object_index};"
            f"{obj.rail_index};{obj.position_y};"
            f"{obj.yaw};{obj.pitch};{obj.roll};"
        )

        return "\n".join(lines) + "\n"
