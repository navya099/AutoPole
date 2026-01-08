# 테스트
from config.catalog.bracket.bracket_type_enum import BracketBaseType, BracketInstallType
from core.BRACKET.bracket_specs import BracketSpec
from core.BRACKET.brackrt_fittings.bracket_fitting_manager import BracketFittingManager
from core.BRACKET.brackrt_fittings.messenger_wire_placement import MessengerWirePlacement
from core.BRACKET.brackrt_fittings.steady_arm_placer import SteadyArmPlacement
from core.POLE.poledata import PolePlaceDATA
from core.POLE.polegroup import PoleGroup
from core.POLE.polegroup_collector import PoleGroupCollection
from utils.util import Direction


def test_steady_arm_fitting_for_I_bracket():
    #더미 정보
    pos = 1234

    # 1. 더미 브래킷
    bracket = BracketSpec(
        bracket_type=BracketBaseType.I,
        install_type=BracketInstallType.OPG,
        gauge=3.0,
        direction=Direction.LEFT,
        name="TEST",
        index=123
    )

    # 2. 더미 전주 속성
    pole = PolePlaceDATA()
    pole.pos=pos
    pole.direction=Direction.LEFT
    pole.gauge=3.0

    pole.brackets.append(bracket)

    # 3. 컬렉션 및 그룹 구성
    collection = PoleGroupCollection()
    group = collection.new_group(pos)
    group.add_pole(trackidx=0, pole=pole)

    # 4. 피팅 실행
    manager = BracketFittingManager()
    manager.run(collection)

    # 5. 검증
    # 최소 2개여야 함
    assert len(pole.fittings) == 2

    # 타입별 검증
    assert any(isinstance(f, SteadyArmPlacement) for f in pole.fittings)
    assert any(isinstance(f, MessengerWirePlacement) for f in pole.fittings)

    steady = [f for f in pole.fittings if isinstance(f, SteadyArmPlacement)]
    messenger = [f for f in pole.fittings if isinstance(f, MessengerWirePlacement)]

    assert len(steady) == 1
    assert len(messenger) == 1

    print('테스트 통과 !')
    for fit in pole.fittings:
        print(f' 코드 = {fit.code}')
        print(f' 브래킷 코드 = {fit.bracket_index}')
        print(f'편위 = {fit.stagger}')

test_steady_arm_fitting_for_I_bracket()