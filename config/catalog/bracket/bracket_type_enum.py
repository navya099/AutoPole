from enum import Enum

class BracketBaseType(Enum):
    I = "I"
    O = "O"
    F = "F"

class BracketVariant(Enum):
    SHORT = "S"
    LONG = "L"
    NONE = ""

class BracketSpecialType(Enum):
    AJ = "AJ"     # Air Joint
    AS = "AS"     # Air Section
    TN = "TN"     # Tunnel Special
    NONE = ""

class BracketInstallType(Enum):
    OPG = "OPG"
    TN = "TN"
    NONE = ""