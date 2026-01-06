from core.WIRE.wire_type import WireType


class WireElement:
    def __init__(
        self,
        wire_type: WireType,
        start_ref,
        index: int =0,
        end_ref=None,
        meta=None,

    ):
        self.type = wire_type
        self.start_ref = start_ref      # PoleRefData
        self.end_ref = end_ref          # PoleRefData | None
        self.meta = meta or {}
        self.index = index  # ★ 핵심