from config.catalog.bracket.bracket_type_enum import BracketSpecialType, BracketBaseType, BracketVariant
from core.AIRJOINT.airjoint_cluster import AirJointCluster
from core.AIRJOINT.airjoint_state import AirJointState
from core.BRACKET.bracket_policy import BracketPolicy
from core.BRACKET.bracket_specs import BracketSpec
from core.POLE.poledata import PolePlaceDATA


class AIRJOINTPolicy(BracketPolicy):
    def decide_airjoint(
            self,
            cluster: AirJointCluster,
            pole_map: dict[tuple[float, int], PolePlaceDATA],
            group_index_map: dict[tuple[float, int], int],
            speed: int
    ) -> dict[tuple[float, int], list[BracketSpec]]:

        results = {}

        cluster_pos_index = {
            pos: idx for idx, pos in enumerate(cluster.positions[:5])
        }

        track_indices = {
            track for (pos, track) in pole_map.keys()
            if pos in cluster.positions
        }

        for track_index in track_indices:
            first_pos, second_pos, third_pos, fourth_pos, end_pos = cluster.positions[:5]

            first_key = (first_pos, track_index)
            if first_key not in pole_map:
                continue

            first_group_index = group_index_map[first_key]

            merged: dict[int, list[BracketSpec]] = {}

            # pole별 spec 생성
            merged.update(
                self.first_pole_process(
                    first_group_index,
                    first_pos,
                    pole_map[first_key],
                    speed
                )
            )

            merged.update(
                self.second_pole_process(
                    second_pos,
                    pole_map[(second_pos, track_index)],
                    speed
                )
            )

            merged.update(
                self.third_pole_process(
                    third_pos,
                    pole_map[(third_pos, track_index)],
                    speed
                )
            )

            merged.update(
                self.forth_pole_process(
                    fourth_pos,
                    pole_map[(fourth_pos, track_index)],
                    speed
                )
            )

            merged.update(
                self.end_pole_process(
                    merged[first_pos:first_pos + 1] if False else merged[first_pos],
                    end_pos
                )
            )

            # ✅ 여기서 AJ 인덱스 확정
            for pos, specs in merged.items():
                aj_idx = cluster_pos_index[pos]
                self._assign_aj_index(
                    specs,
                    cluster_index=aj_idx,
                    airjoint_id=cluster.number
                )
                results[(pos, track_index)] = specs

        return results

    def first_pole_process(self, index, pos, pole, speed):
        #fisrtpole은 시작전주라서  BracketPolicy의 deice_base 로직 재사용
        return {pos : [self._decide_base(index, pole, speed)]}

    def second_pole_process(self, pos, pole, speed):
        if pole.track_index == 0:
            f_spec = self.decide_f_bracket(
                pole, speed, variant=BracketVariant.SHORT
            )
            i_spec = self.decide_aj_bracket(
                default_type=BracketBaseType.I,
                pole=pole,
                speed=speed
            )
            specs = [f_spec, i_spec]

        elif pole.track_index == 1:
            o_spec = self.decide_aj_bracket(
                default_type=BracketBaseType.O,
                pole=pole,
                speed=speed
            )
            f_spec = self.decide_f_bracket(
                pole, speed, variant=BracketVariant.SHORT
            )
            specs = [f_spec, o_spec]

        else:
            specs = []

        return {pos: specs}

    def third_pole_process(self, pos, pole, speed):
        if pole.track_index == 0:
            aj_spec1 = self.decide_aj_bracket(default_type=BracketBaseType.I,pole=pole, speed=speed)
            aj_spec2 = self.decide_aj_bracket(default_type=BracketBaseType.O, pole=pole, speed=speed)
        elif pole.track_index == 1:
            aj_spec1 = self.decide_aj_bracket(default_type=BracketBaseType.O, pole=pole, speed=speed)
            aj_spec2 = self.decide_aj_bracket(default_type=BracketBaseType.I, pole=pole, speed=speed)
        else:
            aj_spec1 = []
            aj_spec2 = []
        return {pos: [aj_spec1, aj_spec2]}

    def forth_pole_process(self, pos, pole, speed):
        if pole.track_index == 0:
            spec1 = self.decide_f_bracket(pole, speed, variant=BracketVariant.LONG)
            spec2 = self.decide_aj_bracket(default_type=BracketBaseType.O, pole=pole, speed=speed)
        elif pole.track_index == 1:
            spec1 = self.decide_f_bracket(pole, speed, variant=BracketVariant.LONG)
            spec2 = self.decide_aj_bracket(default_type=BracketBaseType.I, pole=pole, speed=speed)
        else:
            spec1 = []
            spec2 = []
        return {pos : [spec1, spec2]}

    def end_pole_process(self, specs: list[BracketSpec], pos):
        # 시작 전주와 동일한 브래킷 세트 사용
        return {pos: specs}


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

    def _assign_aj_index(self, specs, cluster_index, airjoint_id):
        for order, spec in enumerate(specs):
            spec.airjoint = AirJointState(
                airjoint_id=airjoint_id,
                cluster_index=cluster_index,
                bracket_order=order
            )

