from typing import Protocol
from core.POLE.poledata import PolePlaceDATA

class PoleLookup(Protocol):
    def get_by_ref(self, ref, track_index) -> PolePlaceDATA | None: ...
