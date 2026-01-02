# 예시 카탈로그
from config.catalog.feeder.crossarm import CROSSARM
from config.catalog.feeder.feeder_material import FeederMaterial
from config.catalog.insulator.insulator import INSULATOR

FEEDER = {
    1234: FeederMaterial(
        code=1234,
        name="급전선 조립체(폴리머애자)",
        crossarms=[CROSSARM[0]],  # 1선용 완철
        insulators=[INSULATOR[1]],  # 지지 애자
        lines=1
    ),
    1249: FeederMaterial(
        code=1249,
        name="급전선 조립체 터널용(폴리머애자)",
        crossarms=[],  # 2선용 완철
        insulators=[INSULATOR[1]],  # 현수 애자
        lines=1
    ),
    597: FeederMaterial(
        code=597,
        name="급전선 조립체 고속철도용(토공)",
        crossarms=[],  # 포완철
        insulators=[],  # 지지 + 현수
        lines=1,
    ),
598: FeederMaterial(
        code=598,
        name="급전선 조립체 고속철도용(터널)",
        crossarms=[],  # 포완철
        insulators=[],  # 지지 + 현수
        lines=1,
    ),
}