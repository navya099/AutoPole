from typing import Protocol

class Exporter(Protocol):
    name: str
    def export(self, ctx): ...
