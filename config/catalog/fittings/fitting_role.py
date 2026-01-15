from enum import Enum, auto

class FittingRole(Enum):
    AIRJOINT_MESSENGER = auto()
    INVALID_LIFT_MESSENGER = auto()
    INVALID_LIFT_CONTACT = auto()
    STEADYARM_LEFT = auto()
    STEADYARM_RIGHT = auto()
