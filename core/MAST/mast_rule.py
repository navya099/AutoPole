class MastRuleSet:
    @staticmethod
    def select_code(speed: int, structure: str) -> int:
        if speed >= 350:
            return MastRuleSet._high_speed(structure)
        else:
            return MastRuleSet._low_speed(structure)

    @staticmethod
    def _low_speed(structure: str) -> int:
        return {
            '토공': 1370,
            '교량': 1376,
            '터널': 1400,
        }[structure]

    @staticmethod
    def _high_speed(structure: str) -> int:
        return {
            '토공': 619,
            '교량': 620,
            '터널': 621,
        }[structure]
