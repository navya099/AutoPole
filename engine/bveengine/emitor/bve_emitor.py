from typing import Protocol
from engine.interface.railwatir import RailwayIR
from core.bve_element import BVEFreeobj

class BVEEmitter(Protocol):
    def emit(self, ir: RailwayIR) -> BVEFreeobj: ...
