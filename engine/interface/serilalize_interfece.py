from abc import ABC, abstractmethod

from engine.interface.railwatir import RailwayIR


class SerializationEngine(ABC):

    @abstractmethod
    def begin(self): ...

    @abstractmethod
    def emit(self, ir: RailwayIR): ...

    @abstractmethod
    def end(self): ...
