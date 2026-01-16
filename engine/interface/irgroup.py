from dataclasses import dataclass, field

from engine.interface.irguopkey import IRGroupKey
from engine.interface.railwatir import RailwayIR

@dataclass
class IRGroup:
    key: IRGroupKey
    irs: list[RailwayIR] = field(default_factory=list)
    meta: dict = field(default_factory=dict)
    # ─────────────────────
    # group-level behavior
    # ─────────────────────

    def add(self, ir: RailwayIR):
        self.irs.append(ir)

    def sort(self):
        self.irs.sort(key=lambda ir: ir.category)

    def is_empty(self) -> bool:
        return not self.irs
