from core.POLE.poledata import PolePlaceDATA
from engine.bveengine.bveengine import BveEngine
from engine.interface.railwatir import RailwayIR
from engine.interface.serilalize_interfece import SerializationEngine


class BVEExporter:
    def __init__(self):
        self.engine = BveEngine()
        self.name = 'BVEExporter'

    def export(self, groups: list[RailwayIR]):
        self.engine.begin()

        for group in sorted(groups, key=lambda g: g.key.pos):
            self.engine.emit_group(group)

        return self.engine.end()
