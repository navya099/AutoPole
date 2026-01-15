from config.catalog.fittings.bracket_fittings import FittingCatalog
from config.catalog.fittings.fitting_role import FittingRole
from core.BRACKET.brackrt_fittings.fitting_type_enum import FittingTypeEnum
from core.BRACKET.brackrt_fittings.steady_arm import SteadyArmFitting
from core.BRACKET.brackrt_fittings.steady_arm_placer import SteadyArmPlacement
from utils.util import TrackSide


class AirJointSteadyArmFitting(SteadyArmFitting):
    """에어조인트 구간별 편위 테이블"""
    STAGGER_RULE = {
            1: [-0.3, -0.1], # f,aj
            2: [-0.1, 0.1], # aj,aj
            3: [0.1, 0.3], # aj f
    }
    FIRST = 0
    LAST = 4
    def fit(self, pole, bracket_spec, speed):
        #편위계산

        stagger = self.cal_stagger(bracket_spec)
        arm_install_direction = self.define_arm_install_direction(bracket_spec)
        mat = self.get_mat(arm_install_direction, speed)
        return SteadyArmPlacement(
            pole_pos=pole.pos,
            bracket_index=bracket_spec.index,
            side=arm_install_direction,
            code=mat.code,
            stagger=stagger,
            type=FittingTypeEnum.SteadyArm
        )

    def cal_stagger(self, bracket_spec):
        if bracket_spec.airjoint.cluster_index in {self.FIRST, self.LAST}:
            stagger = self.fit_standard_stagger(bracket_spec) #시작 끝 전주는 표준편위
        else: #에어조인트구간은 테이블 적용
            try:
                stagger = self.STAGGER_RULE[
                    bracket_spec.airjoint.cluster_index
                ][bracket_spec.airjoint.bracket_order]
            except KeyError:
                raise ValueError(
                    f"Invalid AJ stagger rule: "
                    f"cluster={bracket_spec.airjoint.cluster_index}, "
                    f"order={bracket_spec.airjoint.bracket_order}"
                )
        return  stagger

    def get_mat(self, arm_install_direction, speed):
        if arm_install_direction == TrackSide.Inner:
            return FittingCatalog.get(speed, FittingRole.STEADYARM_LEFT)
        elif arm_install_direction == TrackSide.Outer:
            return FittingCatalog.get(speed, FittingRole.STEADYARM_RIGHT)
        else:
            return FittingCatalog.get(speed, FittingRole.INVALID_LIFT_MESSENGER)
