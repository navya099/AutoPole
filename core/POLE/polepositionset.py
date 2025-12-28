from dataclasses import dataclass

@dataclass
class PolePositionSet:
    positions: list[int]
    post_numbers: list[tuple[int, str]]
    post_types: list[tuple[int, str]]
    airjoints: list[tuple[int, str]]
