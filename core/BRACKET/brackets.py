from dataclasses import dataclass

@dataclass
class Bracket:
    inner: int  # I형
    outer: int  # O형
    flat_short: int  # F(S)
    flat_long: int  # F(L)
    airjoint_inner: int  # AJ-I
    airjoint_outer: int  # AJ-O


@dataclass
class GaugeBracketSet:
    gauge: float
    bracket: Bracket


@dataclass
class InstallTypeBracket:
    install_type: str  # 예: OpG, Tn
    gauge_brackets: dict[float, GaugeBracketSet]  # 게이지별 브래킷 정보


@dataclass
class PoleStructure:
    design_speed: int
    typename: str
    install_brackets: dict[str, InstallTypeBracket]  # OpG, Tn 등



