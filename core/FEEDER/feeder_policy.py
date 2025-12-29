from core.FEEDER.feeder_spec import FeederSpec


class FeederPolicy:
    def __init__(self):
        self.map = {
            ('토공', 150): 1234,
            ('토공', 250): 1234,
            ('토공', 350): 597,
            ('교량', 150): 1234,
            ('교량', 250): 1234,
            ('교량', 350): 597,
            ('터널', 150): 1249,
            ('터널', 250): 1249,
            ('터널', 350): 598,
        }

    def decide(self, pole, speed) -> list[FeederSpec]:
        specs: list[FeederSpec] = []

        # 기본 단일 급전선
        base = self.decide_single(pole, speed)
        specs.append(base)

        return specs

    def decide_single(self, pole, speed):
        index = self.map.get(
            (pole.current_structure, speed),
            1234
        )

        return FeederSpec(
            index=index,
            name='급전선 지지물',
            direction=pole.direction,
            offset=pole.gauge * pole.direction.value
        )
