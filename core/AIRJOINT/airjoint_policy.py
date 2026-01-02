from config.catalog.bracket.bracket_type_enum import BracketSpecialType, BracketBaseType, BracketVariant
from core.AIRJOINT.airjoint_cluster import AirJointCluster
from core.BRACKET.bracket_policy import BracketPolicy
from core.BRACKET.bracket_specs import BracketSpec
from core.POLE.poledata import PolePlaceDATA


class AIRJOINTPolicy(BracketPolicy):
    def decide_airjoint(
        self,cluster: AirJointCluster,
        pole_map: dict[int, PolePlaceDATA],
        group_index_map: dict[int, int],
        speed: int
    ) -> dict[int, list[BracketSpec]]:

        first_pos, second_pos, third_pos, fourth_pos, end_pos = cluster.positions[:5]
        first_index = group_index_map[first_pos]

        first_spec = self.first_pole_process(first_index, first_pos, pole_map[first_pos], speed)
        second_spec = self.second_pole_process(second_pos, pole_map[second_pos], speed)
        third_spec = self.third_pole_process(third_pos, pole_map[third_pos], speed)
        forth_spec = self.forth_pole_process(fourth_pos, pole_map[fourth_pos], speed)
        end_spec = self.end_pole_process(first_spec, end_pos)

        return {**first_spec , **second_spec , **third_spec , **forth_spec , **end_spec}
    def first_pole_process(self, index, pos, pole, speed):
        #fisrtpole은 시작전주라서  BracketPolicy의 deice_base 로직 재사용
        return {pos : [self._decide_base(index, pole, speed)]}

    def second_pole_process(self, pos, pole, speed):
        #항상 FI
        f_spec = self.decide_f_bracket(pole, speed, variant=BracketVariant.SHORT)
        i_spec = self.decide_default_bracket(default_type=BracketBaseType.I, pole=pole, speed=speed)

        return {pos : [f_spec, i_spec]}

    def third_pole_process(self, pos, pole, speed):

        aj_spec1 = self.decide_aj_bracket(default_type=BracketBaseType.O,pole=pole, speed=speed)
        aj_spec2 = self.decide_aj_bracket(default_type=BracketBaseType.O, pole=pole, speed=speed)
        return {pos: [aj_spec1, aj_spec2]}

    def forth_pole_process(self, pos, pole, speed):
        f_spec = self.decide_f_bracket(pole, speed, variant=BracketVariant.LONG)
        o_spec = self.decide_default_bracket(default_type=BracketBaseType.O, pole=pole, speed=speed)

        return {pos : [o_spec, f_spec]}

    def end_pole_process(self, spec, pos):
        # endpole은 시작전주와 동일
        value = next(iter(spec.values()))  # 첫 번째 값 꺼내기
        return {pos: value}

    def decide_f_bracket(self, pole, speed, variant):
        """F브래킷 생성용 정책"""
        current_type = BracketBaseType.F
        # 설치 구분 판별
        install_type = self.get_installtype(pole.ref.structure_type)
        # 설치 방향
        direction = self.resolve_bracket_direction(pole.direction, install_type)
        #AJ타입지정
        specialtype = BracketSpecialType.NONE
        # 코드 찾기
        mat = self.catalog.find_one(
            speed=speed,
            base_type=current_type,
            special_type=specialtype,
            install_type=install_type,
            variant=variant,
            gauge=pole.gauge,
        )

        # 결과 반환
        return BracketSpec(
            bracket_type=current_type,
            install_type=install_type,
            gauge=mat.gauge,
            direction=direction,
            name=mat.name,
            index=mat.code
        )

    def decide_default_bracket(self, default_type, pole, speed):
        """기본브래킷 생성용 정책"""

        # 설치 구분 판별
        install_type = self.get_installtype(pole.ref.structure_type)
        # 설치 방향
        direction = self.resolve_bracket_direction(pole.direction, install_type)

        # 코드 찾기
        mat = self.catalog.find_one(
            speed=speed,
            base_type=default_type,
            special_type=BracketSpecialType.NONE,
            install_type=install_type,
            variant=BracketVariant.NONE,
            gauge=pole.gauge,
        )

        # 결과 반환
        return BracketSpec(
            bracket_type=default_type,
            install_type=install_type,
            gauge=mat.gauge,
            direction=direction,
            name=mat.name,
            index=mat.code
        )

    def decide_aj_bracket(self, default_type ,pole, speed):
        """AJ브래킷 생성용 정책"""
        # 설치 구분 판별
        install_type = self.get_installtype(pole.ref.structure_type)
        # 설치 방향
        direction = self.resolve_bracket_direction(pole.direction, install_type)
        # AJ타입지정
        specialtype = BracketSpecialType.AJ
        # 코드 찾기
        mat = self.catalog.find_one(
            speed=speed,
            base_type=default_type,
            special_type=specialtype,
            install_type=install_type,
            variant=BracketVariant.NONE,
            gauge=pole.gauge,
        )

        # 결과 반환
        return BracketSpec(
            bracket_type=default_type,
            install_type=install_type,
            gauge=mat.gauge,
            direction=direction,
            name=mat.name,
            index=mat.code
        )