from enum import Enum, auto

class FittingRole(Enum):
    NORMAL_MESSENGER = auto() #일반용 조가선 지지금구
    AIRJOINT_MESSENGER = auto() #에어조인트 조가선 지지금구
    INVALID_LIFT_MESSENGER = auto() #무효인상용 조가선 지지금구
    INVALID_LIFT_CONTACT = auto()
    STEADYARM_LEFT = auto()
    STEADYARM_RIGHT = auto()
