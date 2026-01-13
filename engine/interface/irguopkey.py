from dataclasses import dataclass

@dataclass(frozen=True)
class IRGroupKey:
    track: int
    pos: float
    post_number: int | None = None
