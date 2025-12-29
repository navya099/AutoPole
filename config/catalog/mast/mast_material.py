from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MastMaterial:
    code: int
    name: str
    type: str
    length: float
    diameter: Optional[float] = None
    thickness: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None

