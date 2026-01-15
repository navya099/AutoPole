from core.bve_element import BVEFreeobj
from engine.bveengine.emitor.bracket_emitor import BracketEmitter
from engine.bveengine.emitor.feeder_emitor import FeederEmitter
from engine.bveengine.emitor.fittin_emitor import BracketFittingsEmitter
from engine.bveengine.emitor.mast_emitor import MastEmitter
from engine.bveengine.emitor.wire_emitor import WireEmitter
from engine.interface.irgroup import IRGroup
from engine.interface.railwatir import RailwayIR
from engine.interface.serilalize_interfece import SerializationEngine

from utils.util import format_distance

class BveEngine(SerializationEngine):

    def __init__(self):
        self.lines = []
        self.emitters = {
            "mast": MastEmitter(),
            "feeder": FeederEmitter(),
            "bracket": BracketEmitter(),
            "fittings" : BracketFittingsEmitter(),
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

    def emit_group(self, group: IRGroup):

        self.lines.append(
            f",;{group.key.post_number}호주 / Track {group.key.track} / STA. {format_distance(group.key.pos)}")

        for ir in group.irs:
            self.emit(ir)

    def end(self):
        self.lines.append(",; BVE END")
        return "\n".join(self.lines)

    def serialize(self, obj: BVEFreeobj, comment: str = '') -> str:
        lines = []

        if comment:
            lines.append(f',;{comment}')

        lines.append(
            f',;{obj.name},;\n'
            f'{obj.track_position}\n'
            f".freeobj {obj.rail_index};{obj.object_index};"
            f"{obj.position_x};{obj.position_y};"
            f"{obj.yaw};{obj.pitch};{obj.roll};"
        )

        return "\n".join(lines) + "\n"
