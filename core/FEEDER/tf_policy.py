from core.FEEDER.feeder_spec import FeederSpec


class TFPolicy:
    def decide(self, pole, speed) -> list[FeederSpec]:
        if not self._is_tf_required(pole):
            return []

        return [
            FeederSpec(
                type="TF",
                index=self._get_tf_index(pole, speed),
                name="보조급전선 지지물",
                direction=pole.direction,
                offset=self._calc_offset(pole)
            )
        ]

    def _is_tf_required(self, pole) -> bool:
        return (
            pole.current_structure == "터널"
            or pole.ispreader
            or pole.track_index >= 2
        )

    def _get_tf_index(self, pole, speed):
        raise NotImplementedError('_get_tf_index 미구현')
    def _calc_offset(self, pole):
        raise NotImplementedError('_calc_offset 미구현')