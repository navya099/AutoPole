from core.POLE.poledata import PolePlaceDATA
from engine.bveengine.bveengine import BveEngine
from engine.interface.railwatir import RailwayIR
from engine.interface.serilalize_interfece import SerializationEngine


class BVEExporter:
    def __init__(self):
        self.engine = BveEngine()
        self.name = 'BVEExporter'

    def export(self, irs: list[RailwayIR]):
        self.engine.begin()

        for ir in irs:
            self.engine.emit(ir)

        return self.engine.end()
