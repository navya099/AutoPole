import random

class PoleUtils:
    @staticmethod
    def generate_postnumbers(lst: list[int]) -> list[tuple[int, str]]:
        postnumbers = []
        prev_km = -1
        count = 0

        for number in lst:
            km = number // 1000  # 1000으로 나눈 몫이 같은 구간
            if km == prev_km:
                count += 1  # 같은 구간에서 숫자 증가
            else:
                prev_km = km
                count = 1  # 새로운 구간이므로 count를 0으로 초기화

            postnumbers.append((number, f'{km}-{count}'))

        return postnumbers

    @staticmethod
    def distribute_pole_spacing_flexible(
            start_km: float, end_km: float, spans: tuple[int, ...] = (45, 50, 55, 60)
    ) -> list[int]:
        """
        45, 50, 55, 60m 범위에서 전주 간격을 균형 있게 배분하여 전체 구간을 채우는 함수
        마지막 전주는 종점보다 약간 앞에 위치할 수도 있음.

        :param start_km: 시작점 (km 단위)
        :param end_km: 끝점 (km 단위)
        :param spans: 사용 가능한 전주 간격 튜플 (기본값: 45, 50, 55, 60)
        :return: 전주 간격 리스트, 전주 위치 리스트
        """
        if spans is None:
            spans = (45, 50, 55, 60)

        start_m = int(start_km)  # km → m 변환
        end_m = int(end_km)

        positions = [start_m]
        selected_spans = []
        current_pos = start_m

        while current_pos < end_m:
            possible_spans = list(spans)  # 사용 가능한 간격 리스트 (45, 50, 55, 60)
            random.shuffle(possible_spans)  # 랜덤 배치

            for span in possible_spans:
                if current_pos + span > end_m:
                    continue  # 종점을 넘어서면 다른 간격을 선택

                positions.append(current_pos + span)
                selected_spans.append(span)
                current_pos += span
                break  # 하나 선택하면 다음으로 이동

            # 더 이상 배치할 간격이 없으면 종료
            if current_pos + min(spans) > end_m:
                break

        return positions

    @staticmethod
    def find_post_number(lst, pos):
        for arg in lst:
            if arg[0] == pos:
                return arg[1]