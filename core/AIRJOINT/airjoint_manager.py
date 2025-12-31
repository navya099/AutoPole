from core.AIRJOINT.airjoint_enum import AirJoint

class AirjointManager:
    @staticmethod
    def define_airjoint_section(positions: list[int]) -> list[tuple[int, str]]:
        """
        에어조인트(AirJoint) 위치를 정의하는 정적 메서드.

        주어진 전주 위치 목록(positions) 중에서 특정 간격(airjoint_span = 1600m)을 기준으로,
        조건을 만족하는 지점부터 최대 5개의 전주 위치에 에어조인트 태그를 할당하여 리스트로 반환한다.

        조건:
            - 현재 위치가 airjoint_span의 배수(±100m 허용 오차)와 가까운 경우에만 에어조인트 설정.

        에어조인트 태그 순서:
            - START, POINT_2, MIDDLE, POINT_4, END

        Args:
            positions (list[int]): 전주 위치(정수값, m단위) 리스트

        Returns:
            list[tuple[int, str]]: (위치, 에어조인트 태그) 쌍의 리스트
        """
        airjoint_list: list[tuple[int, str]] = []
        airjoint_span: int = 1600  # 에어조인트 설치 간격(m)

        def is_near_multiple_of_number(number: int, tolerance: int = 100) -> bool:
            """
            숫자가 주어진 간격(airjoint_span)의 배수에 근접한지 판단하는 내부 함수.

            Args:
                number (int): 판별할 숫자
                tolerance (int, optional): 허용 오차. 기본값은 100.

            Returns:
                bool: 배수에 근접하면 True, 아니면 False
            """
            remainder = number % airjoint_span
            return number > airjoint_span and (remainder <= tolerance or remainder >= (airjoint_span - tolerance))

        i = 0
        while i < len(positions) - 1:
            pos = positions[i]
            if is_near_multiple_of_number(pos):
                next_values = positions[i + 1:min(i + 6, len(positions))]
                tags = [
                    AirJoint.START.value,
                    AirJoint.POINT_2.value,
                    AirJoint.MIDDLE.value,
                    AirJoint.POINT_4.value,
                    AirJoint.END.value
                ]
                airjoint_list.extend(list(zip(next_values, tags[:len(next_values)])))
                i += 5  # 다음 다섯 개를 건너뜀
            else:
                i += 1

        return airjoint_list