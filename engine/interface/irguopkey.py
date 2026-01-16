from dataclasses import dataclass

@dataclass(frozen=True)
class IRGroupKey:
    track: int
    pos: float
