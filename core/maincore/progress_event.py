from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class ProgressType(Enum):
    UPDATE = auto()
    FINISHED = auto()
    ERROR = auto()


@dataclass
class ProgressEvent:
    type: ProgressType
    message: str
    percent: int = 0
    step: Optional[int] = None
    total: Optional[int] = None
    exception: Optional[Exception] = None
