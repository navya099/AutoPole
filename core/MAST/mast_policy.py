from core.MAST.mast_spec import MastSpec


class MastPolicy:
    _MAST_TABLE = {
        150: {
            '토공': (1370, 'P-10"x7t-9m'),
            '교량': (1376, 'P-12"x7t-8.5m'),
            '터널': (1400, '터널하수강'),
        },
        250: {
            '토공': (1370, 'P-10"x7t-9m'),
            '교량': (1376, 'P-12"x7t-8.5m'),
            '터널': (1400, '터널하수강'),
        },
        350: {
            '토공': (619, 'H형주-208X202'),
            '교량': (620, 'H형주-250X255'),
            '터널': (621, '터널하수강'),
        }
    }

    def decide(self, pole, speed) -> list[MastSpec]:
        return self._decide_per_track(pole, speed)

    def _decide_per_track(self, pole, speed) -> list[MastSpec]:
        return [self._decide_single(pole, speed)]

    def _decide_single(self, pole, speed) -> MastSpec:
        index, name = self.get_mast_type(speed, pole.current_structure)
        return MastSpec(index, name, pole.direction)

    def get_mast_type(self, speed: int, current_structure: str) -> tuple[int, str]:
        mast_data = self._MAST_TABLE.get(speed)
        if mast_data is None:
            raise ValueError(f"지원하지 않는 속도: {speed}")

        result = mast_data.get(current_structure)
        if result is None:
            raise ValueError(f"지원하지 않는 구조물: {current_structure}")

        mast_index, mast_name = result
        return mast_index, mast_name
