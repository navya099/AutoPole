from dataclasses import dataclass
from typing import Callable

from core.maincore.stepkey import StepKey


@dataclass
class ProcessStep:
    message: str
    action: Callable[[], None]
    key: StepKey = StepKey.NORMAL
    enabled: bool = True
